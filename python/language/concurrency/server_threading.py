# thread solvation of blocking


from socket import *
from fib import fib


def fib_server_1(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)

    while True:
        client, addr = sock.accept()  # blocking
        print(f"Connection {addr=}")
        fib_handler_1(client)

from threading import Thread
def fib_server_2(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)

    while True:
        client, addr = sock.accept()
        print(f"Connection {addr=}")
        Thread(target=fib_handler_1, args=(client,), daemon=True).start()

from concurrent.futures import ProcessPoolExecutor as Pool
def fib_server_3(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    
    while True:
        client, addr = sock.accept()  
        print(f"Connection {addr=}")
        Thread(target=fib_handler_2, args=(client,), daemon=True).start()


def fib_handler_1(client: socket):
    while True:
        req = client.recv(100)  # blocking
        if not req:
            break
        n = int(req)
        print(f"{n=}")
        result = fib(n)
        resp = str(result).encode() + b'\n'
        client.send(resp)  # blocking
    print("Closed")

pool = Pool(4)
def fib_handler_2(client: socket):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        print(f"{n=}")
        future = pool.submit(fib, n)
        result = future.result()
        resp = str(result).encode() + b'\n'
        client.send(resp)
    print("Closed")


# fib_server_1(('', 25000))
# fib_server_2(('', 25000))
fib_server_3(('', 25000))
# use: `netcat localhost 2500` to chech fib_server
