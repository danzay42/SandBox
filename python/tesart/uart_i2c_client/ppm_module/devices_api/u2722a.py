from .visa_device_api import VisaDevice, QtCore


class U2722A(VisaDevice):
	"""
	Keysight Source Measure Unit
	"""
	channels = (1, 2, 3)
	
	def device_list(self):
		instruments = []
		for instr in super(U2722A, self).device_list():
			if instr.startswith('USB'):
				type_, vid, pid, *_ = instr.split('::')
				if int(vid) == 0x0957 and int(pid) == 0x4118:
					instruments.append(instr)
		return instruments
	
	def set(self, channel, state, voltage=3.3, m_current=10):
		self.opc_err(f"OUTP OFF, (@{channel})")
		if state:
			if m_current > 120:
				raise ValueError(f"High current value {m_current} (<=120mA)")
			v_range = min([v for v in [2, 20] if v >= abs(voltage)])
			i_range = min([i for i in [1e-3, 10e-3, 100e-3, 1, 10, 120] if i >= m_current])
			
			self.opc_err(f"SOUR:VOLT:RANG R{v_range}V, (@{channel})")
			self.opc_err(f"SOUR:CURR:RANG R{i_range}mA, (@{channel})")
			self.opc_err(f"SOUR:CURR:LIM {m_current}mA, (@{channel})")
			self.opc_err(f"SOUR:VOLT {voltage}, (@{channel})")
			self.opc_err(f"OUTP ON, (@{channel})")
	
	def get(self, channel):
		voltage = self.query(f"MEAS:VOLT? (@{channel})")
		current = self.query(f"MEAS:CURR? (@{channel})")
		return float(voltage), float(current)


if __name__ == '__main__':
	dev = U2722A()
	devs = dev.device_list()
	print(devs)
	
	if devs:
		for i, instr in enumerate(devs):
			dev.connect_device(instr)
			dev.rst()
			for ch in dev.channels:
				dev.set(state=True, channel=ch, voltage=ch)
				print(instr, ch, dev.get(channel=ch), sep='\t|\t')
