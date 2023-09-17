from ppm_module.devices_api.hmp4040 import HMP4040
from ppm_module.ui.power import Ui_Form, QtWidgets
from ppm_module.devices.visa_device import VisaDeviceGui


class PowerSource(VisaDeviceGui, Ui_Form):
	device: HMP4040
	
	def __init__(self, *args, **kwargs):
		super(PowerSource, self).__init__(device=HMP4040, *args, **kwargs)
		self.event_timer.setInterval(200)
	
	def connect_signals(self):
		super(PowerSource, self).connect_signals()
		self.btn_power.toggled.connect(self.turn_sequence)
		self.event_timer.timeout.connect(self.check_power)
		self.btn_1.toggled.connect(lambda state: self.channel_config(1))
		self.btn_2.toggled.connect(lambda state: self.channel_config(2))
		self.btn_3.toggled.connect(lambda state: self.channel_config(3))
		self.btn_4.toggled.connect(lambda state: self.channel_config(4))
	
	def turn_sequence(self, state):
		self.device.output(state)
		if state:
			self.event_timer.start()
		else:
			self.event_timer.stop()

	def channel_config(self, ch):
		self.device.set(
			getattr(self, f'btn_{ch}').value().isChecked(),
			getattr(self, f'sv_{ch}').value(),
			getattr(self, f'sc_{ch}').value() / 1000)
		
	def check_power(self):
		for ch in self.device.channels:
			if getattr(self, f'btn_{ch}').isChecked():
				u, i = self.device.get(ch)
				getattr(self, f'gv_{ch}').setValue(u)
				getattr(self, f'gc_{ch}').setValue(int(i*1000))
	
	def setupUi(self, widget):
		super(PowerSource, self).setupUi(self)
		Ui_Form.setupUi(self, self.widget_control)
		Ui_Form.retranslateUi(self, self.widget_control)
		self.tree.topLevelItem(0).setText(0, "Источник питания")
		self.state_label.setText("ИП")

		self.table.setColumnWidth(0, 90)
		for column in range(1, self.table.columnCount()):
			self.table.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
		for ch in range(4):
			self.table.setSpan(ch * 3, 0, 2, 1)
			self.table.setSpan(ch * 3 + 2, 0, 1, 3)
			self.table.setRowHeight(ch * 3 + 2, 2)
			self.table.verticalHeader().setSectionResizeMode(ch * 3 + 1, QtWidgets.QHeaderView.Stretch)
			self.table.verticalHeader().setSectionResizeMode(ch * 3, QtWidgets.QHeaderView.Stretch)
			self.table.setCellWidget(ch * 3, 1, getattr(self, 'sv_' + str(ch + 1)))
			self.table.setCellWidget(ch * 3, 2, getattr(self, 'sc_' + str(ch + 1)))
			self.table.setCellWidget(ch * 3 + 1, 1, getattr(self, 'gv_' + str(ch + 1)))
			self.table.setCellWidget(ch * 3 + 1, 2, getattr(self, 'gc_' + str(ch + 1)))
			self.table.setCellWidget(ch * 3, 0, getattr(self, 'btn_' + str(ch + 1)))
	
		self.tree.expandAll()


if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	core = PowerSource()
	core.adjustSize()
	core.show()
	app.exec()
