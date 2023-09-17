from header import *
from src.app_core import Core
from src_1x36.qt_gui import QtGUI
from src_1x36.matrix import Matrix
from src_1x36.app_errors import *


class MatrixApplication(Core):
    GUI: QtGUI
    MATRIX: Matrix

    _save_path = path + '/save_config_136.ini'

    def __init__(self):
        super(MatrixApplication, self).__init__(QtGUI, Matrix)
