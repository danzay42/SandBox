import asyncio
import json
from . import logger


def echo(data):
	logger.debug(f'echo: {data}')
	yield asyncio.sleep(0.1)
	yield data


class AsyncSocketServer:
	handler = None
	timeout = 1
	term = b'\r\n'
	coding = 'utf-8'

	def __init__(self, ip='', port=5000, handler=echo):
		self.ip = ip
		self.port = port
		self.handler = handler

	async def create_server(self):
		"""
		Create server coroutine
		"""
		server = await asyncio.start_server(self.connection_handler, self.ip, self.port)
		async with server:
			try:
				logger.info(f"SERVER {self.__class__.__name__} Start {self.ip}:{self.port}")
				await server.serve_forever()
			except asyncio.CancelledError:
				logger.debug('SERVER: asyncio.CancelledError')

	async def connection_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
		"""
		Connection handler, exists until client is exists
		"""
		client_ip, port = writer.get_extra_info('peername')
		logger.debug(f"SERVER[{self.port}] client: {client_ip, port}")


class AsyncCommandServer(AsyncSocketServer):

	async def read(self, reader: asyncio.StreamReader) -> str | list[str] | None:
		raw_data = await asyncio.wait_for(reader.readuntil(self.term), timeout=self.timeout)
		logger.info(f"SERVER read({len(raw_data)}): {raw_data}")
		return raw_data.decode(self.coding).strip()

	async def write(self, writer: asyncio.StreamWriter, data: str) -> None:
		data = data.encode(self.coding) + self.term
		writer.write(data)
		logger.info(f"SERVER write [{len(data)}]: {data}")
		await writer.drain()

	async def connection_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
		await super(AsyncCommandServer, self).connection_handler(reader, writer)
		while True:
			try:
				if raw_data := await self.read(reader):
					data = json.loads(raw_data)
					result = await self.handler(data)
					if result:
						await self.write(writer, str(result))
			except asyncio.TimeoutError:
				# logger.debug("SERVER: asyncio.TimeoutError")
				continue
			except (asyncio.IncompleteReadError, ConnectionResetError):
				logger.debug("SERVER: asyncio.IncompleteReadError or ConnectionResetError")
				return


class AsyncDataServer(AsyncSocketServer):

	writer: asyncio.StreamWriter = None
	reader: asyncio.StreamReader = None

	async def write(self, data: str):
		if self.writer and not self.writer.is_closing():
			data = data.encode(self.coding)
			self.writer.write(data)
			logger.debug(f"DATA SERVER write {data}")
			await self.writer.drain()

	async def connection_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
		await super(AsyncDataServer, self).connection_handler(reader, writer)
		self.writer = writer
		self.reader = reader


def run(*servers: AsyncSocketServer):
	asyncio.run(asyncio.wait([server.create_server() for server in servers]))


if __name__ == '__main__':
	server1 = AsyncSocketServer(port=5000)
	server2 = AsyncDataServer(port=5001)
	run(server1, server2)

