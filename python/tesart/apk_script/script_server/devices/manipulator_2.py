import asyncio
from . import logger, exceptions, visa, base


bit_ref_set = 0x00020000
bit_in_pos = 0x00080000
bit_move_block = 0x00010000


class Manipulator(base.Manipulator):

	task = 0
	velocity = 50  # 100
	acc = 6  # 16

	def __init__(self, **kwargs):
		super(Manipulator, self).__init__(termination='\r\n', **kwargs)
		for i, axis in enumerate(self.transports):
			axis.write('PROMPT 0')
			axis.write('CLRFAULT')
			axis.write("EN")
			axis.instr.clear()
			if not self.status(axis=i) & bit_ref_set:
				axis.write('MH')

	def info(self, *args, **kwargs):
		info = {f"[{i}]axis": self.position(i) for i, axis in enumerate(self.transports)}
		return info

	def stop(self):
		for ax in self.transports:
			ax.write("STOP")

	def status(self, axis=0):
		self.transports[axis].instr.clear()
		return int(self.transports[axis].query("TRJSTAT").lstrip('H'), 16)

	def stopped(self, axis=0):
		status = self.status(axis)
		return bool(status & bit_in_pos) and not bool(status & bit_move_block)

	def move(self, pos: float = 0, axis: int = 0):
		logger.info(f"MOVE [{axis}]: {pos}")
		self.transports[axis].write(f"ORDER {self.task} {int(pos * 1e4)} {self.velocity} 8192 {self.acc} {self.acc} 0 -1 0 0")
		self.transports[axis].write(f"MOVE {self.task}")

	def position(self, axis: int = 0):
		self.transports[axis].instr.clear()
		return round(float(self.transports[axis].query(f'PFB')), 4) * 1e-4

	async def wait(self, axis: int = 0):
		while not self.stopped(axis):
			await asyncio.sleep(0.01)
