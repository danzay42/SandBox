from ppm_module.devices_api.visa_device_api import VisaDevice
from ppm_module.ui.visa import Ui_Form, QtCore, QtWidgets


class VisaDeviceGui(QtWidgets.QWidget, Ui_Form):
	device: VisaDevice = None
	used = False
	event_timer: QtCore.QTimer
	
	def __init__(self, device=VisaDevice, addr=None, *args, **kwargs):
		super(VisaDeviceGui, self).__init__(*args, **kwargs)
		self.event_timer = QtCore.QTimer(self)
		self.event_timer.setInterval(1000)
		self.device = device()
		self.setupUi(self)
		self.connect_signals()
		self.update_object_names()
		
		if addr:
			self.dev_list.insertItem(0, addr)
			self.dev_list.setCurrentIndex(0)
	
	def connect_signals(self):
		self.device.signal_error.connect(lambda e: [self.event_timer.stop(), print(e)])
		self.cmd.clicked.connect(lambda a: self.device.parse_scpi_cmd(self.response.text()))
		self.rst.clicked.connect(lambda a: self.device.rst())
		self.idn.clicked.connect(lambda: self.response.setText(self.device.idn()))
		self.err.clicked.connect(lambda: self.response.setText(self.device.err()))
		self.dev_list.currentTextChanged.connect(self.connect_device)
		self.dev_list.installEventFilter(self)
	
	def dev_list_update(self):
		current_items = [self.dev_list.itemText(i) for i in range(self.dev_list.count())]
		new_items = self.device.device_list()
		self.dev_list.addItems(set(new_items) - set(current_items))
	
	def connect_device(self, name):
		if self.device.connect_device(name):
			self.state_label.setStyleSheet("background-color: rgba(51, 209, 122, 100)")
			self.used = True
		else:
			self.used = False
			self.state_label.setStyleSheet("background-color: rgba(224, 27, 36, 100)")
			
	def eventFilter(self, target, event):
		if target == self.dev_list:
			if event.type() == QtCore.QEvent.MouseButtonPress:
				self.dev_list_update()
		return False
	
	def setupUi(self, parent):
		super(VisaDeviceGui, self).setupUi(parent)
		self.dev_list.lineEdit().setPlaceholderText('Введите идентификатор...')
		self.tree.topLevelItem(0).setTextAlignment(0, QtCore.Qt.AlignCenter)
		self.tree.topLevelItem(1).setTextAlignment(0, QtCore.Qt.AlignCenter)
		self.tree.setItemWidget(self.tree.topLevelItem(0).child(0), 0, self.widget_connect)
		self.tree.setItemWidget(self.tree.topLevelItem(1).child(0), 0, self.widget_control)
		self.tree.expandAll()
		self.dev_list_update()
	
	def update_object_names(self):
		for w in self.findChildren(QtWidgets.QWidget):
			if w.objectName() and not w.objectName().startswith('qt_'):
				w.setObjectName('_'.join([self.__class__.__name__, w.objectName()]))


if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	core = VisaDeviceGui()
	core.tree.topLevelItem(1).setHidden(True)
	core.adjustSize()
	core.show()
	app.exec_()
	core.close()
