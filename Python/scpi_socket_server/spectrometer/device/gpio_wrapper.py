from .mmaper import MEM

GPIO_WORDS_SIZE = 4
WRITE_REG = 0
READ_REG = 2


class GPIO(MEM):
	
	def __init__(self, offset):
		super(GPIO, self).__init__(offset, GPIO_WORDS_SIZE)
	
	def set_pin(self, state: int):
		self.write_word(WRITE_REG, state)
	
	def get_pin(self) -> int:
		return self.read_word(READ_REG)
	
	def bit_rdy(self, bit=0b1) -> bool:
		return bool(self.get_pin() & bit)

		