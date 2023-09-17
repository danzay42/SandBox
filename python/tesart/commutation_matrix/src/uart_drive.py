from header import *

_pBUF = 2
_pREAD = 0
_pWRITE = 0b1 << 6
_pSTATUS_OK = 0b1 << 5
_pERROR = 0b1 << 4


def _send_bytes(pcb, sw, ch, rw=_pWRITE): return bytes([
    rw | (pcb & 0b1111),                                # lsb
    (0b1 << 7) | ((sw & 0b1111) << 3) | (ch & 0b111),   # msb
])


def _check_recv(send_bytes, recv_bytes):
    if send_bytes[0] & _pERROR:
        raise ConnectionError
    elif not ((send_bytes[0] | _pSTATUS_OK) == recv_bytes[0] and
              send_bytes[1] == recv_bytes[1]):
        raise ValueError


if not DEBUG:
    class UARTDrive(serial.Serial):
        _SERIAL_PORT = '/dev/serial0'
        _SERIAL_PORT_BAUDRATE = 115_200
        _SERIAL_TIMEOUT = 1

        def __init__(self, port=_SERIAL_PORT, speed=_SERIAL_PORT_BAUDRATE):
            super(UARTDrive, self).__init__(port=port,
                                            baudrate=speed,
                                            timeout=self._SERIAL_TIMEOUT,
                                            # parity=serial.PARITY_NONE,
                                            # stopbits=serial.STOPBITS_TWO,
                                            # bytesize=serial.EIGHTBITS,
                                            )
            logger.debug(f"UART connect")

        def __del__(self):
            logger.debug(f"UART disconnect")

        def send(self, board, switch, ch):
            sbytes = _send_bytes(board, switch, ch, _pWRITE)
            self.reset_output_buffer()
            self.reset_input_buffer()
            self.write(sbytes)
            logger.debug(f"UART write: 1[{bin(sbytes[0])}] 2[{bin(sbytes[1])}]")

            rbytes = self.read(size=_pBUF)
            logger.debug(f"UART read_row: {rbytes}")
            logger.debug(f"UART read: 1[{bin(rbytes[0])}] 2[{bin(rbytes[1])}]")

            _check_recv(sbytes, rbytes)

else:
    class UARTDrive:
        def send(self, board, switch, ch):
            sbytes = _send_bytes(board, switch, ch, _pWRITE)
            logger.debug(f"UART write: 1[{bin(sbytes[0])}] 2[{bin(sbytes[1])}]")