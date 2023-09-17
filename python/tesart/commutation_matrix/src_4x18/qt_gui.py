from src.qt_gui import MainWindow
from src_4x18.qt_auto_gui import Ui_mainWindow
from PyQt5.QtWidgets import QRadioButton


class QtGUI(MainWindow):
    auto_gui_object: Ui_mainWindow

    def __init__(self):
        super(QtGUI, self).__init__(Ui_mainWindow)
        for rb in self.findChildren(QRadioButton):
            rb.clicked.connect(self.switch)

        self.show()

    def switch(self):
        name = self.sender().objectName().split('_')
        self.sender().setAutoExclusive(False)
        self.sender().setChecked(False)
        self.sender().setAutoExclusive(True)

        self.signal_switch.emit(int(name[1]), int(name[2]))

    def switch_result(self, sw_, output_):
        rb = getattr(self.auto_gui_object, f'rb_{sw_}_{output_}')
        rb.setChecked(True)
