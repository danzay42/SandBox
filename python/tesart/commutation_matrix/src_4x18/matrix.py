from src.matrix import MatrixBase


class Matrix(MatrixBase):
    MODEL = 'SwitchMatrix_4x18'
    SERIAL_NUMBER = 'RU123456789'
    MANUFACTURE = 'Tesart'
    FIRMWARE_VERSION = 'v1.0'

    BOARDS = [1]
    INPUTS = [1, 2, 3, 4, 5]
    OUTPUTS = range(1, 7)

    PCB = BOARDS
    SWITCHES = INPUTS  # change for order of switches
    CHANNELS = OUTPUTS

    COMMUTATION = None
    SWITCH_STATUS = None

    GEN = SWITCHES[4]
    TX  = SWITCHES[0]
    INJ = SWITCHES[1]
    SA1 = SWITCHES[2]
    SA2 = SWITCHES[3]

    def __init__(self):
        self.COMMUTATION = {input_: self.OUTPUTS[0] for input_ in self.INPUTS}
        self.SWITCH_STATUS = {self.PCB[0]: {switch: self.CHANNELS[0] for switch in self.SWITCHES}}

    def auto_to_manual(self, input_, output_):
        return [(self.BOARDS[0], self.SWITCHES[input_-1], output_), ]
    
    def check_auto_values(self, input_, output_) -> None:
        super(Matrix, self).check_auto_values(input_, output_)
        if input_ == self.GEN:
            if output_ not in self.OUTPUTS[:2]:
                raise ValueError
