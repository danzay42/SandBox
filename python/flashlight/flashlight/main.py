import socket
from .logic import Flashlight
from .serializer import desirealize
from .socket_read import read_block


fl = Flashlight()


def cmds_parser(cmd: str, meta: str):
    match cmd, meta:
        case "ON", _:
            fl.on()
        case "OFF", _:
            fl.off()
        case "COLOR", color:
            fl.color(color)
        case _:
            print("Wrong Arg")


def get_input_data():
    host, port = "127.0.0.1", 9999
    try:
        host = input(f"Host [{host}]: ") or host
        port = input(f"Port [{port}]: ") or port
    except KeyboardInterrupt:
        pass
    return host, int(port)


def run():
    host, port = get_input_data()

    with socket.socket() as sock:
        try:
            sock.connect((host, port))
            while data := read_block(sock):
                parsed_data = desirealize(data)
                if parsed_data is None:
                    continue
                cmds_parser(*parsed_data)
        except ConnectionRefusedError:
            print("Connection Refused, Exit")
        except KeyboardInterrupt:
            print("Exit")

