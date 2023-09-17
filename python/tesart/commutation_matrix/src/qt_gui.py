from header import *


class TranslucentWidget(QWidget):
    def __init__(self, parent=None):
        super(TranslucentWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.move(0, 0)
        self.resize(800, 480)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(QColor("#333333"))
        qp.setBrush(QColor(30, 30, 30, 160))
        qp.drawRect(self.pos().x(), self.pos().y(), self.size().width(), self.size().width())
        qp.end()


class MainWindow(QMainWindow):
    signal_close = pyqtSignal()
    signal_switch = pyqtSignal(int, int)
    signal_show_message = pyqtSignal(str, bool, bool)

    auto_gui_object = None

    msg: QMessageBox = None
    msg_back: TranslucentWidget = None
    msg_timer: QTimer = None

    def __init__(self, auto_gui):
        super(MainWindow, self).__init__()
        self.auto_gui_object = auto_gui()
        self.auto_gui_object.setupUi(self)
        self.signal_show_message.connect(self.show_message)

        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setCursor(Qt.BlankCursor)
        # self.move(0, 0)

    def show_message(self, message: str, error: bool = False, fatal: bool = False):
        if self.msg is None:
            self.msg, self.msg_back, self.msg_timer = QMessageBox(self), TranslucentWidget(self), QTimer()
            self.msg.setWindowFlag(Qt.FramelessWindowHint)
            message_font = QFont()
            message_font.setPointSize(24)
            self.msg.setFont(message_font)
            self.msg.setStandardButtons(QMessageBox.Ok)

            self.msg.buttonClicked.connect(self.msg_back.close)
            self.msg_timer.timeout.connect(self.msg.close)
            self.msg_timer.timeout.connect(self.msg_back.close)

        self.msg.setText(message)
        if not error:
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("Information")
            self.msg_timer.start(5000)
        else:
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setWindowTitle("Error")
            self.msg_timer.start(10000)

        self.msg_back.show()
        self.msg.show()
        if fatal:
            self.msg.exec_()

    def closeEvent(self, a0):
        self.signal_close.emit()

    def switch(self):
        pass

    def switch_result(self, input_, output_):
        pass
