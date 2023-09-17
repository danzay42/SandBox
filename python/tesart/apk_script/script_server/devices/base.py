import asyncio
from .transport import SCPITransport
from . import exceptions


def frange(start: float, stop: float, step: float = 1):
	r = start
	step = abs(step)
	if start <= stop:
		while r <= stop:
			yield r
			r += step
	else:
		while r >= stop:
			yield r
			r -= step


def prange(start: float, stop: float, points: int = 1):
	points = int(abs(points))
	if points <= 1:
		yield start
	else:
		step = (stop - start) / (points-1)
		for i in range(points):
			yield start
			start += step


class BaseDevice:
	transports: list[SCPITransport] = None
	transport: SCPITransport = None

	def __init__(self, transport_type=SCPITransport, **kwargs):
		if addrs := kwargs.get("address"):
			self.transports = []
			for addr in addrs.split(';'):
				transport = transport_type(addr, **kwargs)
				self.transport = transport
				self.transports.append(transport)

	def info(self, *args, **kwargs): ...
	async def wait(self, *args, **kwargs): ...

	async def wait_timeout(self, timeout=2, *args, **kwargs):
		try:
			await asyncio.wait_for(self.wait(*args, **kwargs), timeout=timeout)
		except asyncio.TimeoutError as e:
			raise exceptions.DeviceError(f"{self.__class__.__name__} Timeout over {timeout} sec.\n{str(e)}")

	def wait_block(self, *args, **kwargs):
		asyncio.get_event_loop().run_until_complete(self.wait_timeout(*args, **kwargs))


class Manipulator(BaseDevice):

	def move(self, pos: float = 0, axis: int = 0): ...
	def stop(self): ...
	def position(self, axis: int = 0): ...

	async def move_async(self, pos: float = 0, axis: int = 0, timeout=60):
		self.move(pos, axis)
		await self.wait_timeout(axis=axis, timeout=timeout)
		return str(self.position(axis))

	def move_block(self, pos: float = 0, axis: int = 0, timeout=60):
		return asyncio.get_event_loop().run_until_complete(self.move_async(pos, axis, timeout))


class NetAnalyzer(BaseDevice):

	def config_channels(self, **kwargs): ...
	def config_transmit(self, **kwargs): ...
	def config_receive(self, **kwargs): ...
	def config_receive_range(self, **kwargs): ...
	def get_data(self, channel=None): ...
	def trigger(self, channel=None): ...


class Switch(BaseDevice):

	def output(self, input_=0): ...
	async def switch_async(self, output_=0, input_=0): ...

	def switch(self, output_=0, input_=0):
		return asyncio.get_event_loop().run_until_complete(self.switch_async(output_, input_))

