from .visa_device_api import VisaDevice, QtCore
import threading
import time


class U2761A(VisaDevice):
	"""
	Keysight 20MHz Functional/Arbitrary Waveform Generator
	"""
	signal_thread: threading.Thread = None
	signal_stop = QtCore.pyqtSignal()

	def device_list(self):
		instruments = []
		for instr in super(U2761A, self).device_list():
			if instr.startswith('USB'):
				type_, vid, pid, *_ = instr.split('::')
				if int(vid) == 0x0957 and int(pid) == 0x3C18:
					instruments.append(instr)
		return instruments
	
	def settings(self, ampl=3.3, offset=1.65, m_period=10.0, ds=2):
		self.opc_err(f"FUNC PULS")
		self.opc_err(f"VOLT {ampl / 2} VPP")
		self.opc_err(f"VOLT:OFFS {offset / 2}")
		self.opc_err(f"PULS:PER {m_period / 1000}")
		self.opc_err(f"FUNC:PULS:DCYC {100 / ds}")
		self.wai()
	
	def _run(self, m_timeout):
		self.opc_err("OUTP ON")
		time.sleep(m_timeout / 1000)
		self.opc_err("OUTP OFF")
		self.signal_stop.emit()
	
	def run(self, state=True, m_timeout=1500):
		if state:
			if m_timeout:
				self.signal_thread = threading.Thread(target=self._run, args=(m_timeout,))
				self.signal_thread.start()
			else:
				self.opc_err("OUTP ON")
		else:
			self.opc_err("OUTP OFF")
			self.signal_stop.emit()

	
if __name__ == '__main__':
	dev = U2761A()
	devs = dev.device_list()
	print(devs)
	
	if devs:
		dev.connect_device(devs[0])
		dev.rst()
		dev.settings(offset=0)
		dev.run()
		dev.signal_thread.join()
		dev.run(m_timeout=500)
