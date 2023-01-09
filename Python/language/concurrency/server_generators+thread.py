# generator schedler solvation of blocking

from socket import *
from collections import deque
from select import select
from fib import fib
# from concurrent.futures import ThreadPoolExecutor as Pool
from concurrent.futures import ProcessPoolExecutor as Pool

pool = Pool(4)
tasks = deque()
recv_wait = {}  # mapping sockets -> tasks (generators)
send_wait = {}
future_wait = {}

future_notify, future_event = socketpair()

def future_done(future):
    tasks.append(future_wait.pop(future))
    future_notify.send(b'x')

def future_monitor():
    while True:
        yield 'recv', future_event
        future_event.recv(100)

tasks.append(future_monitor())

def run():
    # while tasks:
    while any([tasks, recv_wait, send_wait]):  # get back what we put into wait
        while not tasks:
            # while No active task to run -> wait for I/O
            can_recv, can_send, [] = select(recv_wait, send_wait, []) # look for ready to work 
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))

        task = tasks.popleft()
        try:
            why, what = next(task)  # <- run to the next yield
            if why == "recv":
                # pass
                # what does it actualy mean to receive -> must go wait somthere -> create recv_wait
                recv_wait[what] = task
            elif why == "send":
                send_wait[what] = task
            elif why == "future":
                future_wait[what] = task
                what.add_done_callback(future_done)
            else:
                raise RuntimeError("arg!")
        except StopIteration:
            print("task done")


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)

    while True:
        yield "recv", sock  # <- yield befor block <- (why,what) im wait here
        client, addr = sock.accept()  # <- blocking
        print(f"Connection {addr=}")
        tasks.append(fib_handler(client))



def fib_handler(client: socket):
    while True:
        yield "recv", client  # <- yield befor block <- (why,what) im wait here
        req = client.recv(100)  # <- blocking
        if not req:
            break
        n = int(req)
        future = pool.submit(fib, n)
        yield 'future', future
        result = future.result()
        resp = str(result).encode() + b'\n'
        yield "send", client  # <- yield befor block <- (why,what) im wait here
        client.send(resp)  # <- blocking
    print("Closed")

tasks.append(fib_server(('', 25000)))
run()
