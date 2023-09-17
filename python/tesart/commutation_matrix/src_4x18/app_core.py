from header import *
from src.app_core import Core
from src_4x18.qt_gui import QtGUI
from src_4x18.matrix import Matrix
from src_4x18.app_errors import *


class MatrixApplication(Core):
    GUI: QtGUI
    MATRIX: Matrix

    _save_path = path + '/save_config_418.ini'

    def __init__(self):
        super(MatrixApplication, self).__init__(QtGUI, Matrix)
    
    def cmd_parse(self, cmd: str):
        try:
            if cmd.startswith('STATE:GEN'):
                return self.gen_config(cmd.lstrip('STATE:GEN').split(','))
            elif cmd.startswith('STATE:SA'):
                return self.sa_config(cmd.lstrip('STATE:SA').split(','))
            else:
                return super(MatrixApplication, self).cmd_parse(cmd)
        except ValueError:
            raise WrongParameter()
        
    def gen_config(self, cmd):
        if len(cmd) == 3:
            gen, tx, inj = map(int, cmd)
            self.MATRIX.check_auto_values(self.MATRIX.TX,  tx)
            self.MATRIX.check_auto_values(self.MATRIX.INJ, inj)
            self.MATRIX.check_auto_values(self.MATRIX.GEN, gen)
            self.auto_switch(self.MATRIX.TX,  tx)
            self.auto_switch(self.MATRIX.INJ, inj)
            self.auto_switch(self.MATRIX.GEN, gen)
        elif len(cmd) == 1 and cmd[0] == "?":
            gen = self.MATRIX.COMMUTATION[self.MATRIX.GEN]
            tx = self.MATRIX.COMMUTATION[self.MATRIX.TX]
            inj = self.MATRIX.COMMUTATION[self.MATRIX.INJ]
            return f"{gen},{tx},{inj}"
        else:
            raise WrongParameter()

    def sa_config(self, cmd):
        if len(cmd) == 2:
            sa1, sa2 = map(int, cmd)
            self.MATRIX.check_auto_values(self.MATRIX.SA1, sa1)
            self.MATRIX.check_auto_values(self.MATRIX.SA2, sa2)
            self.auto_switch(self.MATRIX.SA1, sa1)
            self.auto_switch(self.MATRIX.SA2, sa2)
        elif len(cmd) == 1 and cmd[0] == "?":
            sa1 = self.MATRIX.COMMUTATION[self.MATRIX.SA1]
            sa2 = self.MATRIX.COMMUTATION[self.MATRIX.SA2]
            return f"{sa1},{sa2}"
        else:
            raise WrongParameter()
