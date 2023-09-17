import asyncio
from . import logger, exceptions, visa, base


class Matrix(base.Switch):

	def output(self, input_=0):
		return int(self.transport.send(f'OUTPUT:STATE?'))

	def info(self, *args, **kwargs):
		return str(self.output())

	async def wait(self, output_):
		while output_ != self.output():
			await asyncio.sleep(0.01)

	async def switch_async(self, output_=0, input_=0):
		self.transport.send(f"OUTPUT:STATE {output_}")
		await self.wait_timeout(output_, timeout=5)
