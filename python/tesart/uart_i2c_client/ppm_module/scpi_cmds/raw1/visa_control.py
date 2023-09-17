import pyvisa
import time


def connect2instr(visa_address):
    return True
    global instr
    rm = pyvisa.ResourceManager()
    instr = rm.open_resource(visa_address)
    #del instr.timeout
    instr.timeout = 1000 * 60 * 30
    instr.write_termination = '\n'
    instr.read_termination = '\n'
    
    instr.query(":SYSTem:ERRor?")
    return True;


def send2instr(data):
    print(data)
    return
    global instr
    instr.write(data)
    instr.write("*WAI")
    return instr.query(":SYSTem:ERRor?")


def justsend2instr(data):
    print(data)
    return
    global instr
    instr.write(data)
    

def query2instr(request):
    print(request)
    return "this was query:\n" + request
    
    global instr
    instr.write("*WAI")
    return instr.query(request)


def disconnect2instr():
    return
    global instr
    instr.close


def write(request):
    global instr
    instr.write(request)


def read():
    global instr
    return instr.read()


def wait():
    print('*OPC;*WAI;*OPC?')
    return
    global instr

    while True:
        write('*ESR?')
        result = read()

        if result == '+0':
            break

    time.sleep(0.01)
