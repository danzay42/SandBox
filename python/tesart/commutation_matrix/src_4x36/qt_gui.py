from header import *
from src.qt_gui import MainWindow
from src_4x36.qt_auto_gui import Ui_mainWindow as Ui_main
from src_4x36.qt_auto_gui_1 import Ui_Dialog as Ui_37
from src_4x36.qt_auto_gui_2 import Ui_Dialog as Ui_36


class QtGUI(MainWindow):
    auto_gui_object: Ui_main

    switch_btns = {i: QPushButton for i in range(1, 5)}
    radio_btns = {i: dict() for i in range(1, 5)}

    def __init__(self):
        super(QtGUI, self).__init__(Ui_main)

        for input_ in range(1, 5):
            dialog = QDialog(parent=self, flags=Qt.FramelessWindowHint)

            if input_ in (1, 2):
                auto_gui = Ui_37()
                auto_gui.setupUi(dialog)
                auto_gui.rb_37.setText(f"Conv {input_}")
                self.reg_rb(auto_gui.rb_37, input_, 37, dialog)
            else:
                auto_gui = Ui_36()
                auto_gui.setupUi(dialog)

            dialog_btn = getattr(self.auto_gui_object, f'input_btn_{input_}')
            dialog_btn.setText("Off")
            dialog_btn.clicked.connect(dialog.show)
            auto_gui.btn_close.clicked.connect(dialog.close)

            self.switch_btns[input_] = dialog_btn
            for output_ in range(37):
                self.reg_rb(getattr(auto_gui, f'rb_{output_}'), input_, output_, dialog)

        self.show()

    def reg_rb(self, rb, input_, output_, dialog):
        rb.setObjectName(f'rb_{input_}_{output_}')
        rb.clicked.connect(self.switch)
        rb.clicked.connect(dialog.close)
        self.radio_btns[input_][output_] = rb

    def switch(self):
        input_, output_ = map(int, self.sender().objectName().split('_')[1:])
        self.radio_btns[input_][output_].setAutoExclusive(False)
        self.radio_btns[input_][output_].setChecked(False)
        self.radio_btns[input_][output_].setAutoExclusive(True)

        self.signal_switch.emit(input_, output_)

    def switch_result(self, input_, output_):
        text = 'Off' if output_ == 0 else f'Conv {input_}' if output_ == 37 else str(output_)
        self.radio_btns[input_][output_].setChecked(True)
        self.switch_btns[input_].setText(text)
