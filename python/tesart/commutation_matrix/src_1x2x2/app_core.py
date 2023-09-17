from header import *
from src.app_core import Core
from src_1x2x2.qt_gui import QtGUI
from src_1x2x2.matrix import Matrix
from src_1x2x2.app_errors import *


class MatrixApplication(Core):
    GUI: QtGUI
    MATRIX: Matrix

    _save_path = path + '/save_config_122.ini'

    def __init__(self):
        super(MatrixApplication, self).__init__(QtGUI, Matrix)
