from header import *
from src.app_core import Core
from src_4x36.qt_gui import QtGUI
from src_4x36.matrix import Matrix
from src_4x36.app_errors import *


class MatrixApplication(Core):
    GUI: QtGUI
    MATRIX: Matrix

    _save_path = path + '/save_config_436.ini'

    def __init__(self):
        super(MatrixApplication, self).__init__(QtGUI, Matrix)

    def auto_switch(self, input_, output_):
        if output_ not in [0, 37] and output_ in self.MATRIX.COMMUTATION.values():
            if not self.MATRIX.COMMUTATION[input_] == output_:
                raise OutputBusy()
        super(MatrixApplication, self).auto_switch(input_, output_)

    def _manual_switch(self, board, switch, ch):
        board, switch, ch = self.MATRIX.change_byte(board, switch, ch)
        super(MatrixApplication, self)._manual_switch(board, switch, ch)
