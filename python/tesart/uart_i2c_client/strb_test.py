from __future__ import annotations
import time
import threading
import pyvisa as visa
import pyvisa.constants as visa_constants
from PyQt5 import QtCore


class AbstractDevice(QtCore.QObject):
	transport: visa.resources
	rm: visa.ResourceManager
	signal_connect = QtCore.pyqtSignal(bool)
	signal_send = QtCore.pyqtSignal(str)
	signal_receive = QtCore.pyqtSignal(str)
	signal_error = QtCore.pyqtSignal(str)
	default_timeout = 1000
	
	def __init__(self, rm_back=''):
		super(AbstractDevice, self).__init__()
		self.rm = visa.ResourceManager(rm_back)
	
	def device_list(self):
		return self.rm.list_resources()
	
	def connect_device(self, name):
		try:
			self.transport = self.rm.open_resource(name)
			self.signal_connect.emit(True)
		except visa.Error as exc:
			self.signal_connect.emit(False)
			self.signal_error.emit(str(exc))
	
	def config(self, timeout=None, termination=None):
		if timeout:
			self.transport.timeout = timeout
		if termination:
			self.transport.read_termination = termination
			self.transport.write_termination = termination
	
	def write_bytes(self, raw_data: bytes):
		self.transport: visa.resources.MessageBasedResource
		self.transport.write_raw(raw_data)
	
	def read_bytes(self, size=1):
		self.transport: visa.resources.MessageBasedResource
		return self.transport.read_raw(size)
	
	def send(self, data: str):
		self.transport: visa.resources.MessageBasedResource
		self.transport.write(data)
		self.signal_send.emit(data)
	
	def query(self, data: str):
		self.transport: visa.resources.MessageBasedResource
		self.send(data)
		res = self.transport.read().strip()
		self.signal_receive.emit(res)
		return res


class VisaDevice(AbstractDevice):
	
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
	
	def set_timeout(self, timeout=None):
		self.transport.timeout = timeout or self.default_timeout
	
	def device_cmd_check(self, cmd):
		print(self.err(), cmd, self.transport.resource_name, self.__class__.__name__, sep='\t|\t')
	
	def parse_scpi_cmd(self, cmd: str, timeout: int = None):
		cmd = cmd.strip()
		res = ''
		self.set_timeout(timeout)
		if '?' in cmd:
			res = self.query(cmd)
		else:
			self.opc(cmd)
		self.set_timeout(timeout)
		self.device_cmd_check(cmd)
		return res
	
	def check_err(self):
		res: str = self.err()
		if not res.startswith('+0'):
			raise visa.Error(self.transport.resource_name, self.__class__.__name__, res)
		return res


class U2761A(VisaDevice):
	"""
	Keysight 20MHz Functional/Arbitrary Waveform Generator
	"""
	signal_thread: threading.Thread = None
	signal_stop = QtCore.pyqtSignal()
	
	def settings(self, ampl=3.3, offset=1.65, m_period=10.0, ds=2):
		self.opc(f"FUNC PULS")
		self.opc(f"VOLT {ampl / 2} VPP")
		self.opc(f"VOLT:OFFS {offset / 2}")
		self.opc(f"PULS:PER {m_period / 1000}")
		self.opc(f"FUNC:PULS:DCYC {100 / ds}")
		self.wai()
	
	def _run(self, m_timeout):
		self.send("OUTP ON")
		time.sleep(m_timeout / 1000)
		self.send("OUTP OFF")
		self.signal_stop.emit()
	
	def run(self, state=True, m_timeout=1500):
		if state:
			if m_timeout:
				self.signal_thread = threading.Thread(target=self._run, args=(m_timeout,))
				self.signal_thread.start()
			else:
				self.send("OUTP ON")
		else:
			self.send("OUTP OFF")
			self.signal_stop.emit()


DUT_MODE_WRITE = 0b00
DUT_MODE_READ = 0b01
DUT_MODE_SELECT = 0b10

FPGA_MODE_RST = 0b00
FPGA_MODE_DUT = 0b01
FPGA_MODE_ADC = 0b10
FPGA_MODE_PWM = 0b11

FPGA_DUT_READ = 1 << 5
FPGA_DUT_WRITE = 0
FPGA_DUT_TRIG = 1 << 4

PWM_BITS = 2 ** 5
ADC_BITS = 2 ** 12
ADC_VOLTAGE = 3.3
TMP36_TERM_BIAS = -0.5
TMP36_TERM_K = 0.01
FAN_FULL = 100
FAN_MEDIUM = 50


def get_fpga_bytes(fpga_mode, fpga_data=0, data=None):
	data = data or []
	return bytes([fpga_mode << 6 | 1 + fpga_data + len(data)] + data)


def bytes_str(bytes_: bytes):
	return str(','.join(list(map(hex, bytes_))) + '|' + ','.join(list(map(bin, bytes_))))


class FpgaDev(AbstractDevice):
	
	def connect_device(self, name):
		super(FpgaDev, self).connect_device(name)
		self.transport: visa.resources.SerialInstrument
		self.transport.baud_rate = 115200
		self.transport.stop_bits = visa_constants.StopBits.one
		self.transport.parity = visa_constants.Parity.even
		self.transport.timeout = self.default_timeout
		self.transport.read_termination = ''
		self.transport.write_termination = ''
	
	def write_bytes(self, data):
		super(FpgaDev, self).write_bytes(data)
		print("FPGA WRITE:", bytes_str(data))
		time.sleep(0.01)
	
	def read_bytes(self, size=1):
		time.sleep(0.01)
		data = super(FpgaDev, self).read_bytes(size)
		print("FPGA READ:", bytes_str(data))
		return data
	
	def rst(self):
		self.write_bytes(get_fpga_bytes(FPGA_MODE_RST))
	
	def dut_write(self, dut_data: list):
		dut_data[0] |= DUT_MODE_WRITE
		self.write_bytes(get_fpga_bytes(FPGA_MODE_DUT, FPGA_DUT_WRITE, dut_data))
	
	def dut_read(self, dut_data: list):
		dut_data[0] |= DUT_MODE_READ
		self.write_bytes(get_fpga_bytes(FPGA_MODE_DUT, FPGA_DUT_READ, dut_data))
		data = self.read_bytes(10)
		return bin(data[0])
	
	def dut_select(self, dut_data: list):
		"""clk_sel & trig"""
		dut_data[0] |= DUT_MODE_SELECT
		self.write_bytes(get_fpga_bytes(FPGA_MODE_DUT, FPGA_DUT_TRIG, dut_data))
	
	def set_pwm(self, percent):
		"""FAN_PUR"""
		pwm_data = (percent * PWM_BITS) // 100
		self.write_bytes(bytes([FPGA_MODE_PWM << 6 | pwm_data]))
	
	# self.write(get_fpga_bytes(FPGA_MODE_PWM, pwm_data))
	
	def get_temp(self):
		"""ANALOG_TO_ADC"""
		self.write_bytes(get_fpga_bytes(FPGA_MODE_ADC))
		res = self.read_bytes(2)
		temp_raw = int.from_bytes(res, byteorder='little', signed=True)
		voltage = temp_raw * (2 * ADC_VOLTAGE / ADC_BITS)
		temp = (voltage + TMP36_TERM_BIAS) / TMP36_TERM_K
		return int(temp), voltage
	
	def pulse(self):
		"""SIGN"""
		self.write_bytes(bytes([FPGA_MODE_ADC << 6]))


if __name__ == '__main__':
	dut_fpga = FpgaDev()
	generator = U2761A()
	devices = dut_fpga.device_list()
	print(devices)
	
	dut_fpga.connect_device([dev for dev in devices if 'ASRL' in dev][0])
	generator.connect_device([dev for dev in devices if '0x0957::0x3C18' in dev][0])
	
	generator.settings()
	dut_fpga.pulse()
	generator.run()
