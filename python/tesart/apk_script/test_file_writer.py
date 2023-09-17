import time
import os


def py_writer():
	with open('test_file', 'a') as file:
		for i in range(1000):
			file.write(f"test_line {i}\r\n")
			file.flush()
			print(f"test_line {i}\r\n", end='')
			# time.sleep(1)


if __name__ == '__main__':
	py_writer()
	# with open('test_file', 'w'):
	# 	exit()
	# os.remove('test_file')
