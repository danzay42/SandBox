import time
import os


def py_open():
	with open('test_file', 'r') as file:
		while True:
			text = file.read()
			if text:
				print(text, end='')


def os_open():
	file = os.open('C:/Users/Tesart/Documents/AntestLight/apk_script/test_file', os.O_NONBLOCK)
	while True:
		line = os.read(file, 1024)
		if line:
			print(line)


if __name__ == '__main__':
	py_open()
