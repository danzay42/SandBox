import socket
import json
import time

task_status = {
    "cmd": "status"
}

task_configure = {
    "configure": {
        # "transceiver": {
        #     "address": "TCPIP::192.168.0.5::INSTR",
        #     "freq": [8e9, 12e9, 3],
        #     "bw": 1000,
        #     "power": -10,
        #     "traces": 1,
        #     "channels": 1,
        #     "source_port": 1,
        #     "external": False,
        #     "display": True
        # },
        "manipulator_2": {
            "address": "TCPIP::192.168.0.254::4001::SOCKET;TCPIP::192.168.0.254::4002::SOCKET"
        }
    },
}

task_main = {
    "task": [
        # {"type": "switch", "args": {}},
        {"type": "move", "nested": 0, "args": {"axis": 0, "range": [0, 0, 1]}},
        {"type": "move", "nested": 1, "args": {"axis": 1, "range": [0, 0, 1]}},
        # {"type": "data", "nested": 2, "args": {"freq": [8e9, 9e9, 2], "save_path": None}},
    ]
}

test_ext = b'{  "configure": {"manipulator_2": {      "address": "TCPIP::192.168.0.254::4002::SOCKET;TCPIP::192.168.0.254::4001::SOCKET"    }  }}\r\n'


def parse_task_dict(task_list) -> dict:
    return task_list.pop() | {'task': parse_task_dict(task_list)} if task_list else {}


if __name__ == '__main__':
    # res = parse_task_dict(task_main['task'])
    # print(res)
    # exit()

    HOST = '127.0.0.1'
    PORT = 5000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        s.connect((HOST, PORT))

        # s.sendall(test_ext)
        # print(s.recv(1024))

        for task in [task_configure, task_status]:
        # for task in [task_status]:
            try:
                s.sendall(json.dumps(task).encode() + b'\r\n')
                print(s.recv(1024))
            except TimeoutError:
                print("timeout")
                continue