from .mmaper import MEM

FPGA_WORDS_SIZE = 256
samples_0 = 0x00
samples_1 = 0x01
samples_2 = 0x02
samples_3 = 0x03
buf_ctrl = 0x10

spi_ctrl = 0x11
spi_lsb = 0x12
spi_msb = 0x13
spi_sel = 0x14

inter_lsb = 0x15
inter_msb = 0x16

spi_rx_lsb = 0x80
spi_rx_msb = 0x81


class FPGA(MEM):
	
	def __init__(self, offset):
		super(FPGA, self).__init__(offset, FPGA_WORDS_SIZE)
	
	def get_version(self) -> str:
		return f"{self.read_word(0xfe)}.{self.read_word(0xfd)}.{self.read_word(0xfc)}"
	
	def start_daq(self):
		self.write_word(buf_ctrl, 0b1)
	
	def set_counter(self, c: int):
		raw = c.to_bytes(4, 'little')
		self.write_word(samples_0, raw[0])
		self.write_word(samples_1, raw[1])
		self.write_word(samples_2, raw[2])
		self.write_word(samples_3, raw[3])
	
	def get_counter(self):
		raw_data = [
			self.read_word(samples_0),
			self.read_word(samples_1),
			self.read_word(samples_2),
			self.read_word(samples_3),
		]
		return int.from_bytes(raw_data, 'little')
	
	def set_spi(self, data: int, mask: int):
		self.write_word(spi_lsb, data & 0xff)
		self.write_word(spi_msb, data >> 8 & 0xff)
		self.write_word(spi_sel, mask & 0xff)
		self.write_word(spi_ctrl, 0b1)
	
	def get_spi(self, data: int, mask: int):
		self.set_spi(data, mask)
		raw_data = [
			self.read_word(spi_rx_lsb),
			self.read_word(spi_rx_msb),
		]
		return int.from_bytes(raw_data, 'little')

	def set_integrator(self, value: int):
		self.write_word(inter_lsb, value & 0xff)
		self.write_word(inter_msb, value >> 8 & 0xff)
	
	def get_integrator(self):
		raw_data = [
			self.read_word(inter_lsb),
			self.read_word(inter_msb),
		]
		return int.from_bytes(raw_data, 'little')
