from header import *
from src.app_core import Core
from src_1x2x6.qt_gui import QtGUI
from src_1x2x6.matrix import Matrix
from src_1x2x6.app_errors import *


class MatrixApplication(Core):
    GUI: QtGUI
    MATRIX: Matrix

    _save_path = path + '/save_config_126.ini'

    def __init__(self):
        super(MatrixApplication, self).__init__(QtGUI, Matrix)
