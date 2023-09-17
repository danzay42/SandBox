import pyvisa
import struct

from time import sleep


# ----- INSTRUMENT CONTROL FUNCTIONS -----
# Creating connection to instrument
def connect(visa_address):
    global instrument

    rm = pyvisa.ResourceManager()
    instrument = rm.open_resource(visa_address)

    instrument.chunk_size = 1024
    instrument.timeout = 1000 * 60 * 30
    instrument.write_termination = '\n'
    instrument.read_termination = '\n'

    return read_error()


# Reading bytes from instrument
def read_bytes(block_size):
    global instrument

    return instrument.read_bytes(block_size, chunk_size=block_size+1)


# Reading block of bytes from instrument and converting to int
def read_int(block_size):
    global instrument

    temp = instrument.read_bytes(block_size).decode('ascii')
    return int(temp)


# Reading block of bytes from instrument and converting to float
def read_float(block_size):
    global instrument

    temp = read_bytes(block_size)
    temp = struct.unpack('>f', temp)[0]
    return temp


# Reading error from instrument
def read_error():
    global instrument

    return instrument.query(":SYSTEM:ERROR?")


# Sending data + *WAI to instrument and reading error
def send(data):
    global instrument

    instrument.write(data)
    instrument.write("*WAI")

    err = read_error()
    print(data, '(', err, ')')


# Sending data without [*WAI and reading error]
def send_only(data):
    global instrument

    instrument.write(data)


# Just query to instrument
def send_and_read(data):
    return instrument.query(data)


# Wait function
def wait(sleep_time):
    global instrument

    while True:
        write('*ESR?')

        if read() == '+0':
            break

    sleep(sleep_time)


# Disconnecting from instrument
def disconnect():
    global instrument

    instrument.close()
