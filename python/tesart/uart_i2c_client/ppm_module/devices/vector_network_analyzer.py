from ppm_module.devices.visa_device import VisaDeviceGui, QtWidgets


class VectorNetworkAnalyzer(VisaDeviceGui):
	
	def setupUi(self, widget):
		super(VectorNetworkAnalyzer, self).setupUi(self)
		self.tree.topLevelItem(0).setText(0, "Векторный анализатор цепей")
		self.tree.topLevelItem(1).setHidden(True)
		self.state_label.setText("ВАЦ")
		

if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	core = VectorNetworkAnalyzer()
	core.adjustSize()
	core.show()
	app.exec()
