from src.qt_gui import MainWindow
from src_1x2x2.qt_auto_gui import Ui_mainWindow


class QtGUI(MainWindow):
    auto_gui_object: Ui_mainWindow

    def __init__(self):
        super(QtGUI, self).__init__(Ui_mainWindow)

        self.radio_btns = dict()
        for input_ in range(2):
            self.radio_btns[input_ + 1] = dict()
            for output_ in range(2):
                rb = getattr(self.auto_gui_object, f'rb_{input_+1}_{output_+1}')
                rb.clicked.connect(self.switch)
                self.radio_btns[input_+1][output_+1] = rb

        self.show()

    def switch(self):
        input_, output_ = map(int, self.sender().objectName().split('_')[1:])
        self.radio_btns[input_][output_].setAutoExclusive(False)
        self.radio_btns[input_][output_].setChecked(False)
        self.radio_btns[input_][output_].setAutoExclusive(True)

        self.signal_switch.emit(input_, output_)

    def switch_result(self, input_, output_):
        self.radio_btns[input_][output_].setChecked(True)
