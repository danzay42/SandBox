class MatrixBase:
    MODEL = None
    SERIAL_NUMBER = None
    MANUFACTURE = None
    FIRMWARE_VERSION = None

    BOARDS: list = None
    INPUTS: list = None
    OUTPUTS: list = None

    PCB: list = None
    SWITCHES: list = None
    CHANNELS: list = None

    COMMUTATION: dict = None
    SWITCH_STATUS: dict = None

# ----------------------------------------------------------------------------------------------------------------------
    def check_auto_values(self, input_, output_) -> None:
        if input_ not in self.INPUTS \
                or output_ not in self.OUTPUTS:
            raise ValueError

    def check_manual_values(self, pcb, switch, ch) -> None:
        if pcb not in self.PCB \
                or switch not in self.SWITCHES \
                or ch not in self.CHANNELS:
            raise ValueError

# ----------------------------------------------------------------------------------------------------------------------
    def auto_to_manual(self, input_, output_):
        return []

    def reset(self):
        pack = list()
        for pcb in self.SWITCH_STATUS:
            for switch in self.SWITCH_STATUS[pcb]:
                pack.append((pcb, switch, self.CHANNELS[0]))
        return pack

    def load(self):
        pack = list()
        for input_, output_ in self.COMMUTATION.items():
            pack.extend(self.auto_to_manual(input_, output_))
        return pack

# ----------------------------------------------------------------------------------------------------------------------
    def check_switch(self, pcb, switch, ch) -> bool:
        return ch == self.SWITCH_STATUS[pcb][switch] or False

    def save_switch(self, pcb, switch, ch):
        self.SWITCH_STATUS[pcb][switch] = ch

# ----------------------------------------------------------------------------------------------------------------------
    def check_commutation(self, input_, output_):
        return output_ == self.COMMUTATION[input_] or False

    def save_commutation(self, input_, output_):
        self.COMMUTATION[input_] = output_
