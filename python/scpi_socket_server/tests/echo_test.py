import pyvisa as visa


def test_remote(ip='172.16.128.150', port=5025):
	rm = visa.ResourceManager()
	instr = rm.open_resource(f"TCPIP::{ip}::{port}::SOCKET")
	instr.read_termination = instr.write_termination = '\r\n'
	# instr: visa.resources.MessageBasedResource
	
	for i in range(10):
		print('echo:', instr.query('auuuu'))


if __name__ == '__main__':
	test_remote('127.0.0.1', 5025)
