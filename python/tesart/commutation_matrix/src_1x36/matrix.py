from src.matrix import MatrixBase


class Matrix(MatrixBase):
    MODEL = 'SwitchMatrix_1x36'
    SERIAL_NUMBER = 'RU123456789'
    MANUFACTURE = 'Tesart'
    FIRMWARE_VERSION = 'v1.0'

    BOARDS = [1]
    INPUTS = [1]
    OUTPUTS = range(1, 37)

    PCB = BOARDS
    SWITCHES = [6, 8, 9, 10, 5, 2, 1]
    CHANNELS = [0, 1, 2, 3, 4, 5, 6]

    COMMUTATION = None
    SWITCH_STATUS = None

    # ------------------------------------------------------------------------------------------------------------------
    _CFG_SWITCH_COMMUTATION = {
        # main switch output: matrix outputs according to output_switch order
        CHANNELS[1]: [32, 31, 22, 23, 24, 33],
        CHANNELS[2]: [29, 28, 19, 20, 21, 30],
        CHANNELS[3]: [11, 10, 1, 2, 3, 12],
        CHANNELS[4]: [14, 13, 4, 5, 6, 15],
        CHANNELS[5]: [17, 16, 7, 8, 9, 18],
        CHANNELS[6]: [35, 34, 25, 26, 27, 36]
    }

    def __init__(self):
        self.COMMUTATION = {self.INPUTS[0]: self.OUTPUTS[0]}
        self.SWITCH_STATUS = {PCB: {SWITCH: self.CHANNELS[0]
                                    for SWITCH in self.SWITCHES}
                              for PCB in self.PCB}

    # ------------------------------------------------------------------------------------------------------------------
    def _cmt_main_switch(self, output_):
        board = self.BOARDS[0]
        switch = self.SWITCHES[0]
        if output_ == 0:
            return [(board, switch, 0)]
        else:
            for channel, outputs in self._CFG_SWITCH_COMMUTATION.items():
                if output_ in outputs:
                    return [(board, switch, channel)]
            else:
                return []

    def _cmt_switch(self, output_):
        board = self.BOARDS[0]
        for channel, outputs in self._CFG_SWITCH_COMMUTATION.items():
            if output_ in outputs:
                switch = self.SWITCHES[channel]
                switch_channel = self._CFG_SWITCH_COMMUTATION[channel].index(output_) + 1
                return [(board, switch, switch_channel)]
        else:
            return []
    # ------------------------------------------------------------------------------------------------------------------

    def auto_to_manual(self, input_, output_):
        self.check_auto_values(input_, output_)
        pack = list()
        pack.extend(self._cmt_main_switch(output_))
        pack.extend(self._cmt_switch(output_))
        return pack
