from .visa_device_api import VisaDevice


class HMP4040(VisaDevice):
	"""
	Rohde&Schwarz Power Source
	"""
	channels = (1, 2, 3, 4)
	
	def output(self, state=False):
		self.opc_err(f"OUTP:GEN {int(state)}")
	
	def set(self, channel, state=False, voltage=5, current=0.1):
		self.opc_err(f"INST OUT{channel}")
		self.opc_err(f"OUTP:SEL {int(state)}")
		self.opc_err(f"VOLT {voltage}")
		self.opc_err(f"CURR {current}")
	
	def get(self, channel):
		self.opc_err(f"INST OUT{channel}")
		voltage = self.query("MEAS:VOLT?").strip()
		current = self.query("MEAS:CURR?").strip()
		return float(voltage), float(current)


if __name__ == '__main__':
	dev = HMP4040()
	devs = dev.device_list()
	print(devs)
	if devs:
		dev.connect_device(devs[int(input("select device from list..."))])
		dev.output(True)
		for ch in dev.channels:
			dev.set(channel=ch, state=True, voltage=ch)
