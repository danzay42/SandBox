from visa_control_v2 import *
from math import log

import matplotlib.pyplot as mplot


# 'visa_control_v2' lib command list:
#
#
# connect(visa_address)         - Creating connection to instrument;
#
#
# read_bytes(block_size)        - Reading bytes from instrument
# read_int(block_size)          - Reading block of bytes from instrument
#                                 and converting to int
# read_float(block_size)        - Reading block of bytes from instrument
#                                 and converting to float
# read_error()                  - Reading error from instrument
#
#
# send(data)                    - Sending data + *WAI to instrument and reading error
# send_only(data)               - Sending data without [*WAI and reading error]
# send_and_read(data)           - Just query to instrument
#
#
# disconnect()                  - Disconnecting from instrument


# ----- CONSTANTS -----
FLOAT_SIZE = 4                  # Byte count in float


# ----- VARIABLES -----
visa_address = 'USB0::0x2A8D::0x7F18::MY52320005::0::INSTR'

f0 = 1e9                        # Central frequency            

trig_delay = -1e-06             # Trigger delay

x_width = 4e-05                 # Trace duration


# ----- MAIN FUNCTIONS -----
def setup():
    send('*CLS')
    send('*RST')
    
    send('SENS1:DET:FUNC NORM')                 # Setting normal measurement mode
    send('SENS1:FREQ %g' % (f0))                # Setting central frequency f0
    send('SENS1:AVER OFF')                      # Disabling averaging
    send('SENS1:TRAC:TIME %g' % (x_width))      # Setting duration of trace
    
    send('TRAC1:UNIT DBM')                      # Setting trace units (dbm)

    send('PST1:CCDF:SWE:STATE 0')               # Disabling gated CCDF measurement

    send('CONF1')                               # Configuring calculate block
    send('CALC1:FEED1 "POW:PEAK"')              # Setting measurement mode

    send('TRIG:SOUR EXT')                       # Trigger source - external
    send('TRIG:DEL %g' % (trig_delay))          # Setting trigger delay

    send('TRAC1:STAT 1')                        # Enabling trace


def read_plot_data():  
    send('INIT1:CONT 0')                        # Setting single trigger mode
    
    data = send_and_read('READ1?')              # Beginning data reading

    send_only('TRAC1:DATA? HRES')               # Reading trace data
    
    read_bytes(1)                               # Getting symbol '#'
    
    size = read_int(1)                          # Reading count of bytes which shows count of data bytes
    data_size = read_int(size)                  # Reading count of data bytes

    float_data_size = int(data_size / FLOAT_SIZE)
    float_data = []

    for i in range(float_data_size):
        float_item = read_float(FLOAT_SIZE)     # Reading data
        float_data.append(float_item)

    return float_data


def read_meas_data():
    send('PST:CCDF:STOR:REF')
    print('\nMeasured data:')
    
    pulse_duration = send_and_read('TRAC:MEAS:PULS:DUR?')
    print('Pulse duration = ', pulse_duration)

    avg_power = send_and_read('PST:CCDF:REF:POW:AVER?')
    print('Average power = ', avg_power)

    peak_power = send_and_read('PST:CCDF:REF:POW:PEAK?')
    print('Peak power = ', peak_power)


# ----- MAIN -----
connect(visa_address)
setup()

data = read_plot_data()
mplot.plot(data)

read_meas_data()

disconnect()
mplot.show()
