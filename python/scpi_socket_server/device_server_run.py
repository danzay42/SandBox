from spectrometer import run
from logging_config import *
import sys


if __name__ == '__main__':
    logging.config.dictConfig(LOGCONFIG)
    if len(sys.argv) == 1:
        run()
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'test':
            from tests.local import run
            run()
        elif sys.argv[1] == 'test_echo':
            from spectrometer.server.async_socket import AsyncSocketServer
            AsyncSocketServer().exec()
