from ppm_module.devices_api.fpga import FpgaDev
from ppm_module.ui.tm import Ui_Form, QtCore, QtGui, QtWidgets
from ppm_module.devices.visa_device import VisaDeviceGui

regs_count = 6
bits_count = 8
attenuation_step = 2
attenuation_steps = 2 ** 4
attenuation_max_val = attenuation_steps * attenuation_step
attenuation_items = [str(val) for val in range(0, attenuation_max_val, attenuation_step)]
phase_step = 22.5
phase_steps = 2 ** 4
phase_max_val = phase_steps * phase_step
phase_items = [str(val / 2) for val in range(0, int(2 * phase_max_val), int(2 * phase_step))]


class TransceiverModule(VisaDeviceGui, Ui_Form):
	device: FpgaDev

	def __init__(self, *args, **kwargs):
		super(TransceiverModule, self).__init__(device=FpgaDev, *args, **kwargs)
		self.event_timer.setInterval(1000)
		
	def connect_signals(self):
		super(TransceiverModule, self).connect_signals()
		self.device.signal_error.connect(lambda e: [
			self.btn_temp_control.setChecked(False), self.btn_temp_update.setChecked(False)])
		self.att_box.currentTextChanged.connect(self._attenuation_box)
		for i in range(4):
			getattr(self, f"phs_box_{i}").currentTextChanged.connect(self._phase_box)
			
		self.btn_write.clicked.connect(lambda a: self.device.dut_write(
			[int(self.widget_address.value()) << 2] + [sum(
				[getattr(self, f'data_{reg + 1}_{bit + 1}').isChecked() << bit
				 if hasattr(self, f'data_{reg + 1}_{bit + 1}') else 0
				 for bit in range(bits_count)]) for reg in range(regs_count)]
		))
		self.btn_read.clicked.connect(lambda a: self.status.setText(self.device.dut_read(
			[int(self.widget_address.value()) << 2]
		)))
		self.btn_sel_0.clicked.connect(lambda a: self.device.dut_select([0 << 2]))
		self.btn_sel_1.clicked.connect(lambda a: self.device.dut_select([1 << 2]))
		self.btn_sel_2.clicked.connect(lambda a: self.device.dut_select([2 << 2]))
		self.pwm_slider.valueChanged.connect(self.device.set_pwm)
		self.event_timer.timeout.connect(self.temperature)
		self.event_timer.timeout.connect(self.temperature_control)
		self.btn_temp_update.toggled.connect(
			lambda state: self.event_timer.start() if state else self.event_timer.stop())
	
	def temperature(self):
		temp, voltage = self.device.get_temp()
		self.temperature_current.setValue(temp)
	
	def temperature_control(self):
		if self.btn_temp_control:
			if self.temperature_current.value() > self.temperature_auto.value():
				self.pwm_slider.setValue(100)
			else:
				self.pwm_slider.setValue(50)
	
	def _attenuation_box(self, val):
		val = int(val)
		self.data_4_1.setChecked(val & 2)
		self.data_4_2.setChecked(val & 2)
		self.data_4_3.setChecked(val & 2)
		self.data_4_4.setChecked(val & 2)
		self.data_4_5.setChecked(val & 4)
		self.data_4_6.setChecked(val & 8)
		self.data_4_7.setChecked(val & 16)
	
	def _phase_box(self, val):
		btn = int(self.sender().objectName()[-1])
		reg, shift = 2 + btn // 2, 1 + btn % 2 * 4
		val = int(float(val) // phase_step)
		for i in range(4):
			getattr(self, f'data_{reg}_{shift + i}').setChecked(val & 0b1 << i)
			
	def _add_tree_node(self, parent, text, widget=None, top_item=True):
		item = QtWidgets.QTreeWidgetItem(parent)
		item.setText(0, text)
		brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
		brush.setColor(QtGui.QColor(153, 193, 241, 100))
		if widget:
			child = QtWidgets.QTreeWidgetItem(item)
			self.tree.setItemWidget(child, 0, widget)
		if top_item:
			brush.setColor(QtGui.QColor(153, 193, 241, 200))
			item.setTextAlignment(0, QtCore.Qt.AlignCenter)
			font = QtGui.QFont()
			font.setPointSize(12)
			item.setFont(0, font)
		item.setBackground(0, brush)
		return item
	
	def setupUi(self, form):
		super().setupUi(form)
		Ui_Form.setupUi(self, self.widget_control)
		Ui_Form.retranslateUi(self, self.widget_control)
		
		self.state_label.setText("ППМ")
		self.idn.setEnabled(False)
		self.err.setEnabled(False)
		self.cmd.setEnabled(False)
		self.response.setEnabled(False)
		self.tree.topLevelItem(0).setText(0, "Приемо-передающий модуль")
		self._add_tree_node(self.tree, "Температура и вентилятор", self.widget_fan)
		item = self._add_tree_node(self.tree, "Иследуемое устройство (ИУ)", self.widget_dut)
		self._add_tree_node(item, "Авто конфигурации", self.widget_auto, False)
		self._add_tree_node(item, "Ручная конфигурации", self.widget_manual, False)
		self.att_box.addItems(attenuation_items)
		for i in range(4):
			getattr(self, f"phs_box_{i}").addItems(phase_items)
		
		self.tree.topLevelItem(1).removeChild(self.tree.topLevelItem(1))
		self.widget_control.deleteLater()
		self.tree.expandAll()


if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	core = TransceiverModule()
	core.adjustSize()
	core.show()
	app.exec()
