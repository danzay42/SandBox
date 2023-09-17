from src.matrix import MatrixBase


class Matrix(MatrixBase):
    MODEL = 'FreqConvKL_1x2x6'
    SERIAL_NUMBER = 'RU123456789'
    MANUFACTURE = 'Tesart'
    FIRMWARE_VERSION = 'v1.0'

    BOARDS = [8, ]
    INPUTS = [1, 2, 3, 4, 5, 6]
    OUTPUTS = [2, 1]

    PCB = BOARDS
    SWITCHES = INPUTS
    CHANNELS = OUTPUTS

    COMMUTATION = None
    SWITCH_STATUS = None

    def __init__(self):
        self.COMMUTATION = {input_: self.OUTPUTS[0] for input_ in self.INPUTS}
        self.SWITCH_STATUS = {self.PCB[0]: {switch: self.CHANNELS[0] for switch in self.SWITCHES}}

    def auto_to_manual(self, input_, output_):
        return [(self.BOARDS[0], self.INPUTS[input_-1], self.OUTPUTS[output_-1]), ]
