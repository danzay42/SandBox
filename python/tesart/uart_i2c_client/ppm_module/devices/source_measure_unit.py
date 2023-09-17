from ppm_module.devices_api.u2722a import U2722A
from ppm_module.ui.smu import Ui_Form, QtWidgets
from ppm_module.devices.visa_device import VisaDeviceGui


class SourceMeasureUnit(VisaDeviceGui, Ui_Form):
	device: U2722A
	
	def __init__(self, *args, **kwargs):
		super(SourceMeasureUnit, self).__init__(device=U2722A, *args, **kwargs)
		self.event_timer.setInterval(200)
		
	def connect_signals(self):
		super(SourceMeasureUnit, self).connect_signals()
		self.event_timer.timeout.connect(self.check_power)
		for ch in U2722A.channels:
			getattr(self, f'btn_{ch}').toggled.connect(lambda state, ch=ch: self.turn_sequence(ch, state))
	
	def turn_sequence(self, ch, state):
		self.device.set(ch, state, getattr(self, f'sv_{ch}').value(), getattr(self, f'sc_{ch}').value())
		if state and not self.event_timer.isActive():
			self.event_timer.start()
		elif not state and self.event_timer.isActive():
			self.event_timer.stop()

	def check_power(self):
		for ch in U2722A.channels:
			if getattr(self, f'btn_{ch}').isChecked():
				u, i = self.device.get(ch)
				getattr(self, f'gv_{ch}').setValue(u)
				getattr(self, f'gc_{ch}').setValue(int(i*1000))

	def setupUi(self, widget):
		super(SourceMeasureUnit, self).setupUi(self)
		Ui_Form.setupUi(self, self.widget_control)
		Ui_Form.retranslateUi(self, self.widget_control)
		self.tree.topLevelItem(0).setText(0, "Источник сигналов (ИС)")
		
		self.table.setColumnWidth(0, 90)
		for column in range(1, self.table.columnCount()):
			self.table.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
		for ch in U2722A.channels:
			ch_t = ch - 1
			self.table.setSpan(ch_t * 3, 0, 2, 1)
			self.table.setSpan(ch_t * 3 + 2, 0, 1, 3)
			self.table.setRowHeight(ch_t * 3 + 2, 2)
			self.table.verticalHeader().setSectionResizeMode(ch_t * 3 + 1, QtWidgets.QHeaderView.Stretch)
			self.table.verticalHeader().setSectionResizeMode(ch_t * 3, QtWidgets.QHeaderView.Stretch)
			
			self.table.setCellWidget(ch_t * 3, 1, getattr(self, f'sv_{ch}'))
			self.table.setCellWidget(ch_t * 3, 2, getattr(self, f'sc_{ch}'))
			self.table.setCellWidget(ch_t * 3 + 1, 1, getattr(self, f'gv_{ch}'))
			self.table.setCellWidget(ch_t * 3 + 1, 2, getattr(self, f'gc_{ch}'))
			self.table.setCellWidget(ch_t * 3, 0, getattr(self, f'btn_{ch}'))
		self.widget_table_elements.deleteLater()
		self.tree.expandAll()


class SourceMeasureUnit1(SourceMeasureUnit):
	
	def setupUi(self, widget):
		super(SourceMeasureUnit1, self).setupUi(self)
		self.btn_1.setText("КОНТ")
		self.btn_2.setText("УПР_Р")
		self.tree.topLevelItem(0).setText(0, "Источник сигналов УПР")
		self.state_label.setText('ИС УПР')


class SourceMeasureUnit2(SourceMeasureUnit):
	
	def setupUi(self, widget):
		super(SourceMeasureUnit2, self).setupUi(self)
		self.btn_1.setText("ФАЗ_1\n11.25°")
		self.btn_2.setText("ФАЗ_2\n5.625°")
		self.tree.topLevelItem(0).setText(0, "Источник сигналов ФАЗ")
		self.state_label.setText('ИС ФАЗ')


if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	core = SourceMeasureUnit()
	core.adjustSize()
	core.show()
	app.exec()
