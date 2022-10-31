import socket


def read_block(s: socket.socket):
    res, parentheses_opend, parentheses_closed = b'', 0, 0
    while b := s.recv(1):
        if b == b'{':
            parentheses_opend = 1
            parentheses_closed = 0
            res = b''
        elif b == b'}':
            parentheses_closed = 1
        res += b
        if res and parentheses_opend and parentheses_closed:
            return res


