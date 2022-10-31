import pyvisa as visa
import time


def test_performance(instr, count=100):
	instr.timeout = 10e3
	ts = time.time()
	for i in range(count):
		instr.write(':SYStem:DATA?')
		instr.read_raw((1024 + 3) * 4+2)
	elapsed_time = time.time() - ts
	instr.timeout = 3000
	return elapsed_time, count, count/elapsed_time


def test_remote(ip='172.16.128.150', port=5025):
	rm = visa.ResourceManager()
	instr = rm.open_resource(f"TCPIP::{ip}::{port}::SOCKET")
	instr.read_termination = instr.write_termination
	instr: visa.resources.MessageBasedResource
	
	ss = 125000000
	samples = [ss & 0xff, ss >> 8 & 0xff, ss >> 16 & 0xff, ss >> 24 & 0xff]
	instr.write(f':SYStem:BYTE 0,{samples[0]}')
	instr.write(f':SYStem:BYTE 1,{samples[1]}')
	instr.write(f':SYStem:BYTE 2,{samples[2]}')
	instr.write(f':SYStem:BYTE 3,{samples[3]}')
	
	print('Check idn:', instr.query('*IDN?'))
	instr.write(':SYStem:DUMP?')
	dump = list(instr.read_raw(256+2))
	print(f'Check dump: len={len(dump)}\n{dump}')
	print(f'Check version from dump: {dump[0xfe]}.{dump[0xfd]}.{dump[0xfc]}')
	
	instr.timeout = 10e3
	instr.write(':SYStem:DATA?')
	data = instr.read_raw((1024+3)*4+2)
	print(f'Check data: len={len(data)}\n{data[:10]}')
	
	elapsed_time, count, fps = test_performance(instr)
	print(f'Check performance pylib: FPS={fps}, time={elapsed_time}, count={count}')


if __name__ == '__main__':
	test_remote('172.16.128.150', 5025)
	# test_remote('127.0.0.1', 5025)
