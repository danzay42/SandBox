from .visa_device_api import VisaDevice, QtCore


class N6705C(VisaDevice):
	"""
	Keysight Power Source
	"""
	channels = (1, 2, 3, 4)
	coupled_channels = []
	
	def device_list(self):
		instruments = []
		for instr in super(N6705C, self).device_list():
			if instr.startswith('USB'):
				type_, vid, pid, *_ = instr.split('::')
				if int(vid) == 10893 and int(pid) == 3842:
					instruments.append(instr)
			else:
				instruments.append(instr)
		return instruments
	
	def _couple(self, channel, state):
		if state and channel not in self.coupled_channels:
			self.coupled_channels.append(channel)
		elif not state and channel in self.coupled_channels:
			self.coupled_channels.remove(channel)
		self.opc_err(":OUTP:STAT:COUP:CHAN " + ','.join(map(str, self.coupled_channels)))
		
	def output(self, state=False):
		# self.opc_err(f"OUTP:STAT {int(state)}, (@{self.coupled_channels[0]})")
		self.opc_err(f"OUTP:STAT {int(state)}")
	
	def set(self, channel, state=False, voltage=5, current=0.1):
		self._couple(channel, state)
		self.opc_err(f"VOLT:LEV {voltage},(@{channel});")
		self.opc_err(f":CURR:LEV {current},(@{channel})")
	
	def get(self, channel):
		voltage = self.query(f"MEAS:VOLT? (@{channel})").strip()
		current = self.query(f"MEAS:CURR? (@{channel})").strip()
		return float(voltage), float(current)
	
	
if __name__ == '__main__':
	dev = N6705C()
	devs = dev.device_list()
	
	print(devs)
	if devs:
		dev.connect_device(devs[int(input("select device from list..."))])
		dev.output(True)
		for ch in dev.channels:
			dev.set(channel=ch, state=True, voltage=ch)
