import asyncio
from . import logger, exceptions, visa, base


class Manipulator(base.Manipulator):

	def __init__(self, **kwargs):
		super(Manipulator, self).__init__(termination='\n', **kwargs)
		axis_params = {  # get after Radioline "Scanner" soft initiate move_drive_device
			0: {'SPEeed': 146, 'USPEeed': 4, 'ACCel': 2000},
			1: {'SPEeed': 297, 'USPEeed': 8.1, 'ACCel': 4000},
			2: {'SPEeed': 300, 'USPEeed': 6.66694, 'ACCel': 4000},
			3: {'SPEeed': 1565, 'USPEeed': 4, 'ACCel': 5000},
			4: {'SPEeed': 302, 'USPEeed': 11.5048, 'ACCel': 5000},
			5: {'SPEeed': 157, 'USPEeed': 9.48, 'ACCel': 5000},
		}
		for ax, params in axis_params.items():
			for name, value in params.items():
				self.transport.send(f"AXIS{ax}:{name} {value}")

	def info(self, *args, **kwargs):
		info = {f"[{axis}]{self.transport.send(f'AXIS{axis}:STATus:IDN?')}": self.position(axis)
				for axis in range(int(self.transport.send('SYST:AXESTOT?')))}
		return info

	def move(self, pos: float = 0, axis: int = 0):
		logger.info(f"MOVE [{axis}]: {pos}")
		self.transport.send(f'AXIS{axis}:UMOV:ABS {pos}')

	def stop(self):
		self.transport.send('SYST:STOP')

	def position(self, axis: int = 0):
		return round(float(self.transport.send(f'AXIS{axis}:STATus:UPOS?')), 4)

	async def wait(self, axis: int = 0):
		while not self.transport.send(f'AXIS{axis}:STATus:OPcode?') == '0':
			await asyncio.sleep(0.01)


