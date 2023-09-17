from src.qt_gui import MainWindow
from src_1x36.qt_auto_gui import Ui_mainWindow


class QtGUI(MainWindow):
    auto_gui_object: Ui_mainWindow

    def __init__(self):
        super(QtGUI, self).__init__(Ui_mainWindow)

        self.radio_btns = dict()
        for i in range(1, 37):
            rb = getattr(self.auto_gui_object, f'rb_{i}')
            rb.clicked.connect(self.switch)
            self.radio_btns[i] = rb

        self.show()

    def switch(self):
        output_ = int(self.sender().objectName().split('_')[1])
        self.radio_btns[output_].setAutoExclusive(False)
        self.radio_btns[output_].setChecked(False)
        self.radio_btns[output_].setAutoExclusive(True)

        self.signal_switch.emit(1, output_)

    def switch_result(self, input_, output_):
        self.radio_btns[output_].setChecked(True)
