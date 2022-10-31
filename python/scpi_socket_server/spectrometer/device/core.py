import asyncio
from . import logger
from .mmaper import MEM
from .fpga_wrapper import FPGA
from .gpio_wrapper import GPIO

UART_OFFSET = 0x42C0_0000
GPIO_OFFSET = 0x4120_0000
FPGA_OFFSET = 0x43C0_0000
MEM_OFFSET = 0x4000_0000
MEM_SIZE = 1024 + 3  # spectrum plus integrals size words
DAQ_TIMEOUT_ERROR = 10


class Spectrometer:
	fpga: FPGA
	gpio: GPIO
	mem: MEM
	
	def __init__(self):
		self.fpga = FPGA(FPGA_OFFSET)
		self.gpio = GPIO(GPIO_OFFSET)
		self.mem = MEM(MEM_OFFSET, MEM_SIZE)
	
	async def _read_data(self) -> bytes:
		logger.debug('DAQ Start')
		self.fpga.start_daq()
		while not self.gpio.bit_rdy():
			await asyncio.sleep(100e-6)
		data = self.mem.dump()
		logger.debug(f'DAQ complete! size={len(data)}')
		return data
	
	def read_data(self):
		return asyncio.wait_for(self._read_data(), DAQ_TIMEOUT_ERROR)
