from ppm_module.devices.visa_device import VisaDeviceGui, QtWidgets


class SpectrumAnalyzer(VisaDeviceGui):
	
	def setupUi(self, widget):
		super(SpectrumAnalyzer, self).setupUi(self)
		self.tree.topLevelItem(0).setText(0, "Анализатор спектра")
		self.tree.topLevelItem(1).setHidden(True)
		self.state_label.setText("АС")


if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	core = SpectrumAnalyzer()
	core.adjustSize()
	core.show()
	app.exec()
