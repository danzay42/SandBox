import sys
import mmap
from . import logger

WORD_SIZE = 4


class MEM:
	words_size: int
	_mmap_mem: mmap.mmap = None
	_shift: int
	
	def __init__(self, offset, words_size, file='/dev/mem'):
		shift = offset % mmap.PAGESIZE
		length = words_size * WORD_SIZE + shift
		offset_ = mmap.PAGESIZE * (offset // mmap.PAGESIZE)
		self._shift = shift
		self.words_size = words_size
		logger.debug(f"INIT {self.__class__.__name__}:\n\t"
		             f"offset={hex(offset)} words_size={words_size} file={file}\n\t"
		             f"shift={shift} length={length} offset_mmap={hex(offset_)}")

		with open(file, 'r+b') as fd:
			self._mmap_mem = mmap.mmap(fileno=fd.fileno(),
			                           length=length,
			                           flags=mmap.MAP_SHARED,
			                           prot=mmap.PROT_WRITE | mmap.PROT_READ,
			                           offset=offset_)
			self.seek(0)

	def seek(self, pos: int) -> None:
		logger.debug(f"{self.__class__.__name__} seek: pos={pos} pos_real={self._shift + pos}")
		self._mmap_mem.seek(self._shift + pos)
	
	def read(self, pos, size: int) -> bytes:
		self.seek(pos)
		raw_data = self._mmap_mem.read(size)
		logger.debug(f"{self.__class__.__name__} read: {raw_data}")
		return raw_data
	
	def write(self, pos, bytes_: bytes):
		self.seek(pos)
		self._mmap_mem.write(bytes_)
		logger.debug(f"{self.__class__.__name__} write: {bytes_}")
		self._mmap_mem.flush(0, 0)  # host only works with flush(0, 0) instead flush() ???
	
	def dump(self) -> bytes:
		self.seek(0)
		raw_data = self._mmap_mem.read()
		logger.debug(f"{self.__class__.__name__} dump: size={len(raw_data)}")
		return raw_data
	
	def read_word_row(self, addr) -> bytes:
		return self.read(addr * WORD_SIZE, WORD_SIZE)

	def write_word_row(self, addr, data: bytes):
		self.write(addr * WORD_SIZE, data[:WORD_SIZE])

	def read_word(self, addr) -> int:
		return int.from_bytes(self.read_word_row(addr), sys.byteorder, signed=False)
	
	def write_word(self, addr, data: int):
		self.write_word_row(addr, data.to_bytes(WORD_SIZE, sys.byteorder, signed=False))
	
	def dump_words(self):
		raw_bytes = self.dump()
		return [int.from_bytes(raw_bytes[i:i + WORD_SIZE], sys.byteorder, signed=False)
		        for i in range(0, len(raw_bytes), WORD_SIZE)]
	
	def dump_bytes(self):
		return self.dump()[::WORD_SIZE]
