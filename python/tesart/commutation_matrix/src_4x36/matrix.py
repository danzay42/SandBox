from src.matrix import MatrixBase


class Matrix(MatrixBase):
    MODEL = 'SwitchMatrix_4x36'
    SERIAL_NUMBER = 'RU123456789'
    MANUFACTURE = 'Tesart'
    FIRMWARE_VERSION = 'v1.0'

    BOARDS = [1, 2, 3, 4, 5, 6, 7]
    INPUTS = [1, 2, 3, 4]
    OUTPUTS = range(38)

    PCB = BOARDS
    SWITCHES = [5, 2, 6, 1, 4, 3, 7, 10, 8, 9]
    CHANNELS = [0, 1, 2, 3, 4, 5, 6]

    COMMUTATION = None
    SWITCH_STATUS = None

    # ------------------------------------------------------------------------------------------------------------------
    _CONV_SWITCH = 4  # it must be 4 (! check this after SWITCHES update !)
    _CFG_CONV = {
        # input: b0 switch
        INPUTS[0]: 11,
        INPUTS[1]: 12,
    }
    _CONV_SWITCH_OUT = {
        # input:              to_conv,      to_switch
        _CFG_CONV[INPUTS[1]]: (CHANNELS[4], CHANNELS[3]),
        _CFG_CONV[INPUTS[0]]: (CHANNELS[1], CHANNELS[2]),
    }
    _CFG_B0 = {
        # input: b0 switches
        INPUTS[0]: 10,
        INPUTS[1]: 1,
        INPUTS[2]: 7,
        INPUTS[3]: 6,
    }
    _CFG_BS = {
        # input: bs switches
        PCB[1]: {INPUTS[0]: SWITCHES[2], INPUTS[1]: SWITCHES[3], INPUTS[2]: SWITCHES[1], INPUTS[3]: SWITCHES[0]},
        PCB[2]: {INPUTS[0]: SWITCHES[2], INPUTS[1]: SWITCHES[3], INPUTS[2]: SWITCHES[1], INPUTS[3]: SWITCHES[0]},
        PCB[3]: {INPUTS[0]: SWITCHES[1], INPUTS[1]: SWITCHES[0], INPUTS[2]: SWITCHES[2], INPUTS[3]: SWITCHES[3]},
        PCB[4]: {INPUTS[0]: SWITCHES[1], INPUTS[1]: SWITCHES[0], INPUTS[2]: SWITCHES[2], INPUTS[3]: SWITCHES[3]},
        PCB[5]: {INPUTS[0]: SWITCHES[1], INPUTS[1]: SWITCHES[0], INPUTS[2]: SWITCHES[2], INPUTS[3]: SWITCHES[3]},
        PCB[6]: {INPUTS[0]: SWITCHES[2], INPUTS[1]: SWITCHES[3], INPUTS[2]: SWITCHES[1], INPUTS[3]: SWITCHES[0]},
    }
    _CFG_BS_OUT = {
        # PCB: outputs according to output_switch order
        PCB[1]: [18, 17, 16, 15, 14, 13],
        PCB[2]: [25, 26, 27, 28, 29, 30],
        PCB[3]: [31, 32, 33, 34, 35, 36],
        PCB[4]: [24, 23, 22, 21, 20, 19],
        PCB[5]: [12, 11, 10, 9, 8, 7],
        PCB[6]: [6, 5, 4, 3, 2, 1]
    }
    #             to_switch_out, to_conv_out
    _CFG_SCONV_CH = CHANNELS[0], CHANNELS[1]

    # ## bs commutation ##
    _CFG_BS_SIN_CH = {
        # switch_in: switch_in_outputs
        SWITCHES[0]: [CHANNELS[4], CHANNELS[5], CHANNELS[6], CHANNELS[1], CHANNELS[2], CHANNELS[3]],
        SWITCHES[1]: [CHANNELS[5], CHANNELS[4], CHANNELS[3], CHANNELS[2], CHANNELS[1], CHANNELS[6]],
        SWITCHES[2]: [CHANNELS[3], CHANNELS[4], CHANNELS[5], CHANNELS[6], CHANNELS[1], CHANNELS[2]],
        SWITCHES[3]: [CHANNELS[6], CHANNELS[5], CHANNELS[4], CHANNELS[3], CHANNELS[2], CHANNELS[1]],
    }
    _CFG_BS_SOUT_CH = {
        # switch_out: switch_out_inputs
        SWITCHES[4]: [CHANNELS[3], CHANNELS[6], CHANNELS[2], CHANNELS[5]],
        SWITCHES[5]: [CHANNELS[3], CHANNELS[5], CHANNELS[2], CHANNELS[6]],
        SWITCHES[6]: [CHANNELS[3], CHANNELS[5], CHANNELS[2], CHANNELS[6]],
        SWITCHES[7]: [CHANNELS[3], CHANNELS[5], CHANNELS[2], CHANNELS[6]],
        SWITCHES[8]: [CHANNELS[3], CHANNELS[5], CHANNELS[2], CHANNELS[6]],
        SWITCHES[9]: [CHANNELS[2], CHANNELS[5], CHANNELS[3], CHANNELS[6]],
    }

    def __init__(self):
        self.COMMUTATION = {input_: self.OUTPUTS[0]
                            for input_ in self.INPUTS}

        self.SWITCH_STATUS = {PCB: {SWITCH: self.CHANNELS[0]
                                    for SWITCH in self.SWITCHES}
                              for PCB in self.PCB[1:]}

        type_1 = list(self._CFG_B0.values())
        type_2 = list(self._CFG_CONV.values())
        self.SWITCH_STATUS[self.PCB[0]] = {SWITCH: self.CHANNELS[0]
                                           for SWITCH in type_1 + type_2}

    # ------------------------------------------------------------------------------------------------------------------
    def _cmt_conv(self, input_, output_):
        if input_ in [1, 2]:
            switch = self._CFG_CONV[input_]
            ch = self._CFG_SCONV_CH[0] if output_ == 37 else self._CFG_SCONV_CH[1]
            return [(self.BOARDS[0], switch, ch)]
        else:
            return []

    def _cmt_b0(self, input_, output_):
        b0 = self.BOARDS[0]
        switch = self._CFG_B0[input_]
        if output_ == 0:
            return [(b0, switch, 0)]
        else:
            for pcb, outputs in self._CFG_BS_OUT.items():
                if output_ in outputs:
                    ch = pcb - 1
                    return [(b0, switch, ch)]
            else:
                return []

    def _cmt_bs(self, input_, output_):
        for pcb, outputs in self._CFG_BS_OUT.items():
            if output_ in outputs:
                i_out = outputs.index(output_)
                bs_sw_in = self._CFG_BS[pcb][input_]
                bs_sw_in_ch = self._CFG_BS_SIN_CH[bs_sw_in][i_out]
                i_in = list(self._CFG_BS_SIN_CH.keys()).index(bs_sw_in)
                bs_sw_out = list(self._CFG_BS_SOUT_CH.keys())[i_out]
                bs_sw_out_ch = self._CFG_BS_SOUT_CH[bs_sw_out][i_in]
                return [(pcb, bs_sw_in, bs_sw_in_ch), (pcb, bs_sw_out, bs_sw_out_ch)]
        else:
            return []

    # ------------------------------------------------------------------------------------------------------------------
    def check_auto_values(self, input_, output_):
        super(Matrix, self).check_auto_values(input_, output_)
        if input_ in [3, 4] and output_ == 37:
            raise ValueError

    def check_manual_values(self, pcb, switch, ch):
        super(Matrix, self).check_manual_values(pcb, switch, ch)
        if pcb == self.PCB[0]:
            type_1 = list(self._CFG_B0.values())
            type_2 = list(self._CFG_CONV.values())
            if switch not in type_1 + type_2:
                raise ValueError
            elif (switch in type_2) and (ch not in self._CFG_SCONV_CH):
                raise ValueError

    # ------------------------------------------------------------------------------------------------------------------
    def auto_to_manual(self, input_, output_):
        self.check_auto_values(input_, output_)
        pack = list()
        pack.extend(self._cmt_conv(input_, output_))
        pack.extend(self._cmt_b0(input_, output_))
        pack.extend(self._cmt_bs(input_, output_))
        return pack

    def change_byte(self, pcb, switch, ch):
        pcb_new = pcb - 1
        if pcb == self.PCB[0]:
            if switch in self._CFG_CONV.values():
                switch_new = self._CONV_SWITCH
                ch_new = self._CONV_SWITCH_OUT[switch][ch]
                return pcb_new, switch_new, ch_new
            elif switch in self._CFG_B0.values():
                ch_new = 4 if ch == 5 else 5 if ch == 4 else ch
                return pcb_new, switch, ch_new
        return pcb_new, switch, ch
