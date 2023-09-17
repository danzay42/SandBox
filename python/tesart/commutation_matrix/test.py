import socket
import time
import pyvisa as visa

eof = '\r\n'


def check_base_cmd():
    cmds = [
        '*IDN?',
        '*RST',
        '*OPC?',
        'SYSTEM:ERROR?',
        'SYSTEM:TCPPORT',
        'SYSTEM:CONFIG:IDN11,22,33,44',
        'SYSTEM:CONFIG:IDN',
        'SYSTEM:IPADDRESS192.168.0.105'
    ]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    sock.connect(('192.168.0.100', 5025))

    for i, cmd in enumerate(cmds):
        sock.send((cmd + eof).encode('ascii'))
        if i in [0, 2, 3, 4, 6]:
            print(i, sock.recv(1024))

    sock.close()


def check_port_change():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    sock.connect(('127.0.0.1', 5025))

    for i in range(1, 10):
        sock.send(('SYSTEM:TCPPORT' + str(5025 + i) + eof).encode('ascii'))

        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(0.005)
        sock.connect(('127.0.0.1', 5025 + i))

        sock.send(('SYSTEM:TCPPORT' + eof).encode('ascii'))
        print(sock.recv(1024))

    sock.send(('SYSTEM:TCPPORT5025' + eof).encode('ascii'))

    sock.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(0.005)
    sock.connect(('127.0.0.1', 5025))

    sock.send(('SYSTEM:TCPPORT' + eof).encode('ascii'))
    print(sock.recv(1024))

    sock.close()


def check_switch(matrix):
    a_cmd = 'STATE:SWITCH'
    m_cmd = 'STATE:SWITCH:MANUAL'

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    sock.connect(('127.0.0.1', 5025))

    def check(i, o):
        sock.send((a_cmd + f'{i},{o}' + eof).encode('ascii'))
        sock.send((a_cmd + f'{i}?' + eof).encode('ascii'))
        o_ = int(sock.recv(1024).decode().strip())
        if o_ != o:
            print((i, o), o_)

    if matrix == 1:
        for j in [1, 2]:
            for i in range(1, 7):
                check(i, j)
    elif matrix == 2:
        for i in [1, 2]:
            for o in range(1, 38):
                check(i, o)
        for i in [3, 4]:
            for o in range(1, 37):
                check(i, o)
    elif matrix == 3:
        for o in range(1, 37):
            check(1, o)
    elif matrix == 4:
        for j in [1, 2]:
            for i in [1, 2]:
                check(i, j)

    sock.close()


def manual_control_visa():
    rm = visa.ResourceManager()
    print(rm.list_resources())
    instr = rm.open_resource('TCPIP::109.202.12.15::23000::SOCKET')
    instr.read_termination = instr.write_termination = '\r\n'
    instr.timeout = 5000
    print(instr.query("*IDN?"))
    
    
def manual_control_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    sock.connect(('109.202.12.15', 23000))

    sock.send(("*IDN?" + eof).encode('ascii'))
    print(sock.recv(1024))
    
    sock.close()


def manual_check_4x18():
    instr = visa.ResourceManager().open_resource('TCPIP::109.202.12.15::23000::SOCKET')
    instr.read_termination = instr.write_termination = '\r\n'
    instr.timeout = 1000

    print(instr.query("*IDN?"))
    print(instr.query("STATE:GEN?"))
    print(instr.query("STATE:SA?"))

    instr.write("STATE:GEN1,5,2")  # STATE:GEN[GEN_SWITCH],[TX],[INJ]
    instr.write("STATE:SA1,5")  # STATE:SA[SA1],[SA2]

    print(instr.query("STATE:GEN?"))
    print(instr.query("STATE:SA?"))


def manual_check_4x18_async():
    instr1 = visa.ResourceManager().open_resource('TCPIP::192.168.88.224::5025::SOCKET')
    instr1.read_termination = instr1.write_termination = '\r\n'
    instr1.timeout = 1000

    instr2 = visa.ResourceManager().open_resource('TCPIP::192.168.88.224::5025::SOCKET')
    instr2.read_termination = instr2.write_termination = '\r\n'
    instr2.timeout = 1000
    
    print(instr1.query("*IDN?"))
    print(instr2.query("STATE:GEN?"))
    print(instr1.query("STATE:SA?"))
    
    # instr.write("STATE:GEN1,5,2")  # STATE:GEN[GEN_SWITCH],[TX],[INJ]
    # instr.write("STATE:SA1,5")  # STATE:SA[SA1],[SA2]
    #
    # print(instr.query("STATE:GEN?"))
    # print(instr.query("STATE:SA?"))


def check_ip_port_switch():
    # instr = visa.ResourceManager().open_resource('TCPIP::192.168.88.224::5025::SOCKET')
    # instr.read_termination = instr.write_termination = '\r\n'
    # print(instr.query("*IDN?"))
    # instr.write("SYSTEM:IPADDRESS192.168.88.223;SYSTEM:TCPPORT5020")
    # instr.close()

    instr = visa.ResourceManager().open_resource('TCPIP::192.168.88.223::5020::SOCKET')
    instr.read_termination = instr.write_termination = '\r\n'
    print(instr.query("*IDN?"))
    instr.write("SYSTEM:IPADDRESS192.168.88.224;SYSTEM:TCPPORT5025")
    instr.close()


def check_4x18_errors():
    addr = "TCPIP::192.168.88.224::5025::SOCKET"
    rm = visa.ResourceManager()
    instr: visa.resources.MessageBasedResource = rm.open_resource(addr)
    instr.write_termination = instr.read_termination = '\r\n'

    print(instr.query("*IDN?"))
    while True:
        for g in [1, 2]:
            for i in range(1, 7):
                for j in range(1, 7):
                    instr.write(f"STATE:GEN{g},{i},{j}")
                    res = instr.query("STATE:GEN?")
                    err = instr.query("SYSTEM:ERROR?")
                    print(f"set/get [{res}][{g},{i},{j}]")
                    if not err.startswith('0'):
                        input('...')


def check_1x2x6_errors():
    addr = "TCPIP::192.168.1.14::5025::SOCKET"
    rm = visa.ResourceManager()
    instr: visa.resources.MessageBasedResource = rm.open_resource(addr)
    instr.write_termination = instr.read_termination = '\r\n'

    print(instr.query("*IDN?"))
    instr.write("*RST")
    # print(instr.query("SYSTEM:ERROR?"))

    for i in range(1, 7):
        for o in range(1, 3):
            instr.write(f"STATE:SWITCH{i},{o}")
            res = instr.query(f"STATE:SWITCH{i}?")
            err = instr.query("SYSTEM:ERROR?")
            print(f"err:[{err}] get:[{res}]")
            input('...')


if __name__ == '__main__':
    # manual_control_socket()
    # manual_control_visa()
    # manual_check_4x18_async()
    # manual_check_4x18()
    # check_base_cmd()
    # check_port_change()
    # check_switch(2)
    # check_ip_port_switch()
    # check_4x18_errors()
    check_1x2x6_errors()

