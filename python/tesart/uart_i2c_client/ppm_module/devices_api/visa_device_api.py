import typing
import pyvisa as visa
import pyvisa.constants as visa_constants
from ppm_module.ui.visa import QtCore
from ppm_module import logger


class AbstractDevice(QtCore.QObject):
	transport: typing.Union[visa.resources.MessageBasedResource, visa.Resource] = None
	rm: visa.ResourceManager
	signal_error = QtCore.pyqtSignal(str)
	default_timeout = 3000
	
	def __init__(self, visa_back=''):
		super(AbstractDevice, self).__init__()
		self.rm = visa.ResourceManager(visa_back)
	
	def device_list(self):
		return list(self.rm.list_resources())
	
	def connect_device(self, name) -> bool:
		self.transport = self.rm.open_resource(name)
		# self.transport.read_termination = '\r\n'
		return True
	
	def config(self, timeout=None, termination=None):
		if timeout:
			self.transport.timeout = timeout
		if termination:
			self.transport.read_termination = termination
			self.transport.write_termination = termination
	
	def write_bytes(self, raw_data: bytes):
		self.transport.write_raw(raw_data)

	def read_bytes(self, size=1):
		return self.transport.read_raw(size)
	
	def send(self, data: str):
		try:
			self.transport.write(data)
		except AttributeError:
			self.signal_error.emit('')
			raise Exception('Устройство не подключено')
		logger.debug(data)
	
	def query(self, data: str):
		self.send(data)
		try:
			res = self.transport.read().strip()
		except AttributeError:
			self.signal_error.emit('')
			raise Exception('Устройство не подключено')
		logger.debug(res)
		return res


class VisaDevice(AbstractDevice):
	
	def connect_device(self, name):
		res = False
		# if name in self.device_list():
		try:
			super(VisaDevice, self).connect_device(name)
			self.set_timeout(500)
			self.idn()
			res = True
		except visa.VisaIOError as err:
			self.signal_error.emit(str(err))
		finally:
			self.set_timeout()
		return res

	def idn(self):
		return self.query('*IDN?')
	
	def err(self):
		return self.query('SYST:ERR?')
	
	def rst(self):
		self.send('*CLS;*RST')
		self.wai()
	
	def wai(self):
		self.query("*OPC;*WAI;*OPC?")
	
	def opc(self, cmd):
		self.query(f'*OPC;{cmd};*OPC?')
	
	def opc_err(self, cmd):
		self.opc(cmd)
		return self.err()
		
	def opc_err_check(self, cmd):
		self.opc(cmd)
		res = self.err()
		if not res.startswith('+0'):
			raise visa.Error(self.transport.resource_name, self.__class__.__name__, res)
		
	def set_timeout(self, timeout=None):
		if self.transport:
			self.transport.timeout = timeout or self.default_timeout
	
	def device_cmd_check(self, cmd):
		print(self.err(), cmd, self.transport.resource_name, self.__class__.__name__, sep='\t|\t')
	
	def parse_scpi_cmd(self, cmd: str, timeout: int = None):
		if cmd:
			cmd = cmd.strip()
			res = ''
			self.set_timeout(timeout)
			if '?' in cmd:
				res = self.query(cmd)
			else:
				self.opc(cmd)
			self.set_timeout()
			self.device_cmd_check(cmd)
			return res


if __name__ == '__main__':
	dev = VisaDevice()
	dev.signal_error.connect(print)
	devs = dev.device_list()
	print(devs)
	if len(devs) > 1:
		for i, instr in enumerate(devs):
			if dev.connect_device(instr):
				try:
					print(f"{i})", dev.idn(), dev.err(), '\n', sep='\t|\t')
				except (visa.Error, OSError, ) as e:
					print("Device Error", e, '\n', sep='\t|\t')
