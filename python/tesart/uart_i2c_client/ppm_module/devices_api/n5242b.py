from .visa_device_api import VisaDevice


class N5242B(VisaDevice):
	"""
	Keysight PNA-X Microwave Network Analyzer
	"""
	pass
	

if __name__ == '__main__':
	dev = N5242B()
	print(dev.device_list())
