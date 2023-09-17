import asyncio
import os
import socket

import pyvisa as visa

from . import async_socket, exceptions, logger, devices


class Core:
	status_list: list[str] = []
	active: bool = False
	socket_cmd: async_socket.AsyncCommandServer = None
	socket_data: async_socket.AsyncDataServer = None
	matrix: devices.base.Switch = None
	net_analyzer: devices.base.NetAnalyzer = None
	manipulator: devices.base.Manipulator = None
	task_params: dict = None

	def __init__(self):
		self.parser_dict = {
			"status": self.status,
			"stop": self.stop
		}
		self.socket_cmd = async_socket.AsyncCommandServer(ip='127.0.0.1', port=5000, handler=self.cmd_parser)
		self.socket_data = async_socket.AsyncDataServer(ip='127.0.0.1', port=5001)
		async_socket.run(self.socket_cmd, self.socket_data)
		# async_socket.run(self.socket_cmd)

	def status(self):
		if len(self.status_list) > 0:
			return self.status_list.pop()
		else:
			return '0'

	def stop(self):
		self.active = False

	def connect(self, **kwargs):
		res = {}
		devices_dict = {
			"matrix_1x36": devices.matrix_1x36_1.Matrix,
			"manipulator_1": devices.manipulator_1.Manipulator,
			"manipulator_2": devices.manipulator_2.Manipulator,
			"transceiver": devices.net_analyzer_1.NetAnalyzer,
		}
		for device_name, device_args in kwargs.items():
			try:
				device = devices_dict[device_name](**device_args)
				res[device_name] = bool(device.info())
				if device_name == "matrix_1x36":
					self.matrix = device
				elif device_name in ("manipulator_1", "manipulator_2"):
					self.manipulator = device
				elif device_name == "transceiver":
					self.net_analyzer = device
			except (visa.Error, exceptions.CoreExceptions, Exception) as e:
				logger.error(str(e))
				self.status_list.append(str(e))
				logger.debug(str(self.status_list))
				res[device_name] = False
		return res

	def task_switch(self, **kwargs):
		if self.matrix:
			res = self.matrix.switch(**kwargs)
			yield str(res)

	def task_manipulator(self, **kwargs):
		if self.manipulator:
			axis = kwargs.get("axis", 0)
			if move_range := kwargs.get("range"):
				for pos in devices.base.prange(*move_range):
					yield self.manipulator.move_async(axis=axis, pos=pos)
			else:
				yield str(self.manipulator.position(axis=axis))

	def task_data(self, **kwargs):
		if self.net_analyzer:
			self.net_analyzer.trigger()
			data = self.net_analyzer.get_data()
			self.task_params.update({'data': data})
			with open(os.path.dirname(__file__) + "/../meas.csv", 'a', encoding='utf-8') as fd:
				for line in data:
					if pos := self.task_params.get('pos'):
						save_str = ','.join((pos, line)) + '\r\n'
					else:
						save_str = line + '\r\n'
					fd.write(save_str)
					# fd.flush()
					if self.socket_data:
						yield self.socket_data.write(save_str)

	def task_freq(self, **kwargs):
		if self.net_analyzer:
			self.net_analyzer.config_receive_range(**kwargs)
			yield

	def task_parse_type(self, **kwargs):
		match kwargs['type']:
			case 'switch':
				return self.task_switch(**kwargs['args'])
			case 'move':
				return self.task_manipulator(**kwargs['args'])
			case 'freq':
				return self.task_freq(**kwargs['args'])
			case 'data':
				return self.task_data()

	def task_parse_dict(self, task_list) -> dict:
		if task_list:
			return task_list.pop() | {'task': self.task_parse_dict(task_list)}
		else:
			return {}

	def task_parse_path(self, path):
		if not bool(path):
			path = os.path.dirname(__file__) + '/../MEAS/'
		elif path.endswith('.csv'):
			return path
		os.makedirs(path, exist_ok=True)
		counter = 0
		while os.path.exists(f"{path}/{counter}.csv"):
			counter += 1
		return f"{path}/{counter}.csv"

	def task_configure(self, tasks):
		self.task_params = {}
		for task in tasks:
			task['nested'] = task.get('nested', -1) + 1
		# tasks.sort(key=lambda t: t['nested'], reverse=True)
		tasks.sort(key=lambda t: t['nested'])
		self.task_params.update({
			'data': None,
			'pos': None,
			'tree': self.task_parse_dict(tasks),
		})
		fd = open(os.path.dirname(__file__) + "/../meas.csv", 'w')
		fd.close()

	async def tasks_run(self, task_args):
		if task_args:
			for value in self.task_parse_type(**task_args):
				# logger.info(f'tasks_run: {task_args}')
				if self.active:
					if asyncio.iscoroutine(value):
						value = await value
					if task_args['type'] == 'move':
						self.task_params.update({'pos': value})

					await self.tasks_run(task_args.get('task'))

	async def cmd_parser(self, data: dict):
		try:
			if cmd := data.get("cmd"):
				return self.parser_dict[cmd]()
			elif connect_kwargs := data.get("configure"):
				return self.connect(**connect_kwargs)
			elif tasks := data.get("task"):
				self.task_configure(tasks)
				logger.debug(f'task to process {self.task_params}')
				self.active = True
				await self.tasks_run(self.task_params['tree'])
				self.active = False
				logger.debug('task to process fin')
		except exceptions.CoreExceptions as e:
			logger.debug(str(self.status_list))
			logger.error(str(e))
			self.status_list.append(e.code)
