import asyncio
import time
from typing import Union, List
from header import *

TERMINATION = b'\r\n'
CODING = 'ascii'
INTERFACE = 'eth0' if 'eth0' in netifaces.interfaces() else netifaces.interfaces()[1]


class Worker(QThread):
	def __init__(self, fn, *args, **kwargs):
		super(Worker, self).__init__()
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
	
	def run(self):
		self.fn(*self.args, **self.kwargs)


def echo(data):
	logger.debug(f'echo: {data}')
	return data


class AsyncSocketServer(QObject):
	handler = None
	timeout = 10
	hosts = ''
	port = 5025
	
	IP = '192.168.88.224'
	PORT = str(port)
	MASK = '255.255.255.0'
	GATEWAY = '192.168.88.1'
	
	signal_recv_message = pyqtSignal(object)
	signal_info = pyqtSignal(object)
	
	_server: asyncio.AbstractServer = None
	_server_thread: QThread = None
	
	def __init__(self, hosts=hosts, port=port, handler=echo):
		super().__init__()
		self.hosts = hosts
		self.PORT = str(port)
		self.handler = handler

	def wait_netifaces(self):
		while netifaces.AF_INET not in netifaces.ifaddresses(INTERFACE):
			time.sleep(0.1)
		logger.debug(f"iface await: {netifaces.ifaddresses(INTERFACE)[netifaces.AF_INET]}")
		while netifaces.AF_INET not in netifaces.gateways():
			time.sleep(0.1)
		logger.debug(f"gateway await: {netifaces.gateways()[netifaces.AF_INET]}")

	async def create_server(self):
		"""
		Create server coroutine
		"""
		self._server = await asyncio.start_server(self.connection_handler, self.hosts, self.PORT)
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
			header = b''
			if isinstance(raw_data, bytes):
				# ieee data transfer protocol
				header = str(len(raw_data))
				header = f"#{len(header)}{header}".encode(CODING)
				data = header + raw_data
			else:
				data = raw_data.encode(CODING)
			
			data += TERMINATION
			writer.write(data)
			logger.debug(f"SERVER write({len(data)})")
			
			if isinstance(raw_data, bytes):
				logger.debug(f"{header} : {data[:5] + b' ... ' + data[-5:]}")
			else:
				logger.debug(f"{data}")
			await writer.drain()
	
	async def connection_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
		"""
		Connection handler, exists until client is exists
		"""
		client_ip, port = writer.get_extra_info('peername')
		logger.debug(f"SERVER client open: {client_ip, port}")
		while True:
			try:
				data = await self.read(reader)
				for cmd in data.split(TERMINATION.decode(CODING)):
					await self.write(writer, self.handler(cmd))
			except asyncio.TimeoutError:
				continue
				# logger.debug("SERVER: asyncio.TimeoutError")
			except asyncio.IncompleteReadError:
				# logger.debug("SERVER: asyncio.IncompleteReadError")
				break
		logger.debug(f"SERVER client close: {client_ip, port}")
	
	def exec(self):
		asyncio.run(self.create_server())
		
	def start(self):
		self.set_ip_mask_gateway()
		self._server_thread = Worker(self.exec)
		self._server_thread.start()
		logger.debug("SERVER: thread start")

	def stop(self):
		if self._server:
			self._server.close()
		logger.debug("SERVER: thread stop")
		
	# ------------------------------------------------------------------------------------------------------------------
	def get_ip(self, iface=INTERFACE):
		try:
			ip = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
			logger.debug(f"SERVER: ip:{ip}, etc:{netifaces.ifaddresses(iface)}")
			self.IP = str(ip)
			return ip
		except KeyError as err:
			logger.error(f"SERVER: ip error {str(err)}, info={netifaces.ifaddresses(iface)}")
			return 'Not Found'
	
	def get_mask(self, iface=INTERFACE):
		try:
			mask = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['netmask']
			logger.debug(f"SERVER: mask:{mask}, etc:{netifaces.ifaddresses(iface)}")
			self.MASK = str(mask)
			return mask
		except KeyError as err:
			logger.error(f"SERVER: mask error {str(err)}")
			return 'Not Found'
	
	def get_gateway(self, iface=INTERFACE):
		try:
			gateway, g_iface = netifaces.gateways()['default'][netifaces.AF_INET]
			logger.debug(f"SERVER: gateway:{gateway}, etc:{netifaces.gateways()}")
			self.GATEWAY = str(gateway)
			return gateway
		except KeyError as err:
			logger.error(f"SERVER: gateway error:{str(err)} info:{netifaces.gateways()}")
			return 'Not Found'
	
	def set_ip_mask_gateway(self, ip=None, mask=None, gateway=None):
		ip = self.IP if ip is None else ip
		mask = self.MASK if mask is None else mask
		gateway = self.GATEWAY if gateway is None else gateway
		logger.debug(f"SERVER: set network params: ip={ip}, mask={mask}, gateway={gateway}")
		
		res = subprocess.call(f"ifconfig {INTERFACE} down".split(' '))
		res += subprocess.call(f"ifconfig {INTERFACE} {ip} netmask {mask}".split(' '))
		if (int(ipaddress.ip_address(gateway)) & int(ipaddress.ip_address(mask))) \
				== (int(ipaddress.ip_address(ip)) & int(ipaddress.ip_address(mask))):
			res += subprocess.call(f"ip route add {ip} via {gateway}".split(' '))
			self.GATEWAY = gateway
		res += subprocess.call(f"ifconfig {INTERFACE} up".split(' '))
		
		logger.debug(res)
		self._listen_info()
		self.IP, self.MASK = ip, mask
	
	def get_port(self):
		return self.PORT
	
	def set_port(self, port):
		self.PORT = str(port)
		self.stop()
		self.start()
	
	def set_dhcp(self):
		subprocess.check_call(f"ifconfig {INTERFACE} 0.0.0.0 0.0.0.0 && dhclient".split(' '))
	
	def _listen_info(self):
		info = '\n'.join([
			f"IP: {self.get_ip(INTERFACE)}",
			f"PORT: {self.get_port()}",
			f"MASK: {self.get_mask(INTERFACE)}",
			f"GATEWAY: {self.get_gateway(INTERFACE)}",
		])
		logger.info(info)
		self.signal_info.emit(info)


if __name__ == '__main__':
	AsyncSocketServer().start()
	while True:
		print('One second...')
		time.sleep(1)
