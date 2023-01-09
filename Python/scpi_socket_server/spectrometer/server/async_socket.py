import asyncio
from typing import Union, List
from . import logger


TERMINATION = b'\r\n'
CODING = 'ascii'


def echo(data):
	logger.debug(f'echo: {data}')
	yield asyncio.sleep(0.1)
	yield data


class AsyncSocketServer:
	handler = None
	timeout = 1
	ip = ''
	port = 5025
	
	_server: asyncio.AbstractServer
	_writer: asyncio.StreamWriter
	
	def __init__(self, ip=ip, port=port, handler=echo):
		self.ip = ip
		self.port = port
		self.handler = handler
	
	async def create_server(self):
		"""
		Create server coroutine
		"""
		self._server = await asyncio.start_server(self.connection_handler, self.ip, self.port)
		async with self._server:
			try:
				await self._server.serve_forever()
			except asyncio.CancelledError:
				logger.debug('SERVER: asyncio.CancelledError')
	
	async def read(self, reader: asyncio.StreamReader) -> Union[str, List[str], None]:
		raw_data = await asyncio.wait_for(reader.readuntil(TERMINATION), timeout=self.timeout)
		logger.debug(f"SERVER read({len(raw_data)}): {raw_data}")
		return raw_data.decode(CODING).strip()
	
	async def write(self, writer: asyncio.StreamWriter, raw_data: Union[str, bytes]) -> None:
		if raw_data:
			data = raw_data if isinstance(raw_data, bytes) else raw_data.encode(CODING)
			data += TERMINATION
			writer.write(data)
			if isinstance(raw_data, str):
				logger.debug(f"SERVER write({len(data)}): {data}")
			else:
				logger.debug(f"SERVER write({len(data)}): {data[:5] + b' ... ' + data[-5:]}")
			await writer.drain()
	
	async def connection_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
		"""
		Connection handler, exists until client is exists
		"""
		client_ip, port = writer.get_extra_info('peername')
		logger.debug(f"SERVER client: {client_ip, port}")
		while True:
			try:
				data = await self.read(reader)
				for cmd in data.split(TERMINATION.decode(CODING)):
					for result in self.handler(cmd):
						if asyncio.iscoroutine(result):
							result = await result
						await self.write(writer, result)
			except asyncio.TimeoutError:
				logger.debug("SERVER: asyncio.TimeoutError")
			except asyncio.IncompleteReadError:
				logger.debug("SERVER: asyncio.IncompleteReadError")
				raise
		
	def exec(self):
		"""
		Run server coroutine
		"""
		asyncio.run(self.create_server())
		
	def stop(self):
		self._server.close()


if __name__ == '__main__':
	server = AsyncSocketServer()
	server.exec()
