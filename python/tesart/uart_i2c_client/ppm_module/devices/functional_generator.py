from ppm_module.devices_api.u2761 import U2761A
from ppm_module.ui.fg import Ui_Form, QtWidgets
from ppm_module.devices.visa_device import VisaDeviceGui


class FunctionalGenerator(VisaDeviceGui, Ui_Form):
	device: U2761A
	
	def __init__(self, *args, **kwargs):
		super(FunctionalGenerator, self).__init__(device=U2761A, *args, **kwargs)

	def connect_signals(self):
		super(FunctionalGenerator, self).connect_signals()
		self.btn.clicked.connect(lambda state: [
			self.set_settings(state),
			self.run(state)
		])
		self.device.signal_stop.connect(lambda: self.btn.setChecked(False))

	def set_settings(self, state=True):
		if state:
			self.device.settings(
				self.amplitude.value(),
				self.offset.value(),
				self.period.value(),
				self.duty_cycle.value())

	def run(self, state):
		self.device.run(state, self.delay.value() if self.timeout.isChecked() else 0)

	def setupUi(self, parent):
		super(FunctionalGenerator, self).setupUi(self)
		Ui_Form.setupUi(self, self.widget_control)
		Ui_Form.retranslateUi(self, self.widget_control)
		self.tree.topLevelItem(0).setText(0, "Функциональный генератор")
		self.state_label.setText("ФГ")
		self.tree.expandAll()


if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	core = FunctionalGenerator()
	core.adjustSize()
	core.show()
	app.exec()
