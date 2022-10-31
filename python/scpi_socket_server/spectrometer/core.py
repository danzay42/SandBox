from typing import List
import asyncio
from . import logger, __version__
from . import exceptions, server, scpi, device

TCP_IP_SOCKET = '', 5025
MODEL = 'Spectrometer'
SERIAL_NUMBER = ''
MANUFACTURE = ''
FIRMWARE_VERSION = __version__


class Core:
	server: server.AsyncSocketServer
	scpi: scpi.ScpiParser
	device: device.Spectrometer
	errors_list: List[str]
	tree: dict
	
	def __init__(self):
		self.tree = {
			'*': {
				'IDN?': self.idn,
			},
			':': {
				'SYStem': {
					'ERRor?': self.err,
					'DUMP?': self.dump,
					'BYTE': self.byte,
					'SPI': self.spi,
					'DATA?': self.data,
				}
			},
		}
		self.scpi = scpi.ScpiParser(self.tree)
		self.errors_list = list()
		self.device = device.Spectrometer()
		self.server = server.AsyncSocketServer(*TCP_IP_SOCKET, self.handler)

	def handler(self, data):
		try:
			try:
				for result in self.scpi.parse_cmd(data):
					yield result
			except (AttributeError, TypeError, KeyError) as err:
				raise exceptions.WrongCommand(err)
			except ValueError as err:
				raise exceptions.WrongParameter(err)
			except asyncio.TimeoutError as err:
				raise exceptions.Timeout(err)
		except exceptions.NoError as err:
			self.errors_list.append(repr(err))
			logger.warning(f'CORE ERROR: buf[{len(self.errors_list)}] {repr(err)}')

	def exec(self):
		self.server.exec()
	
	def idn(self):
		return f"{MODEL},{SERIAL_NUMBER},{MANUFACTURE},sw{FIRMWARE_VERSION}_hw{self.device.fpga.get_version()}"
	
	def err(self):
		if self.errors_list:
			return self.errors_list.pop()
		else:
			return repr(exceptions.NoError())
	
	def data(self):
		return self.device.read_data()
	
	def byte(self, addr: str, data: str):
		addr = int(addr)
		if data.isdigit():
			data = int(data)
			self.device.fpga.write_word(addr, data)
		elif data == '?':
			return str(self.device.fpga.read_word(addr))
		else:
			raise exceptions.WrongParameter(f'Byte Wrong parameter: {addr}|{data}')
	
	def spi(self, data, mask, query=None):
		data = int(data)
		mask = int(mask)
		if query:
			if query == '?':
				return str(self.device.fpga.get_spi(data, mask))
			else:
				raise exceptions.WrongParameter(f'SPI Wrong parameter: {data}|{mask}|{query}')
		else:
			self.device.fpga.set_spi(data, mask)
	
	def dump(self):
		return self.device.fpga.dump()
