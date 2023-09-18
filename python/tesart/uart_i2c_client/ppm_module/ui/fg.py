# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/daniil/Documents/TESART_Projects/CAFAR/ppm/ppm_module/ui/fg.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(259, 155)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.duty_cycle = QtWidgets.QDoubleSpinBox(Form)
        self.duty_cycle.setAlignment(QtCore.Qt.AlignCenter)
        self.duty_cycle.setDecimals(1)
        self.duty_cycle.setMinimum(1.0)
        self.duty_cycle.setMaximum(100.0)
        self.duty_cycle.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)
        self.duty_cycle.setProperty("value", 2.0)
        self.duty_cycle.setObjectName("duty_cycle")
        self.gridLayout.addWidget(self.duty_cycle, 5, 1, 1, 1)
        self.amplitude = QtWidgets.QDoubleSpinBox(Form)
        self.amplitude.setAlignment(QtCore.Qt.AlignCenter)
        self.amplitude.setDecimals(1)
        self.amplitude.setMinimum(-10.0)
        self.amplitude.setMaximum(10.0)
        self.amplitude.setSingleStep(0.1)
        self.amplitude.setProperty("value", 3.3)
        self.amplitude.setObjectName("amplitude")
        self.gridLayout.addWidget(self.amplitude, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 5, 0, 1, 1)
        self.period = QtWidgets.QDoubleSpinBox(Form)
        self.period.setAlignment(QtCore.Qt.AlignCenter)
        self.period.setMinimum(0.0)
        self.period.setMaximum(2000000.0)
        self.period.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)
        self.period.setProperty("value", 0.5)
        self.period.setObjectName("period")
        self.gridLayout.addWidget(self.period, 4, 1, 1, 1)
        self.offset = QtWidgets.QDoubleSpinBox(Form)
        self.offset.setAlignment(QtCore.Qt.AlignCenter)
        self.offset.setMinimum(-10.0)
        self.offset.setMaximum(10.0)
        self.offset.setSingleStep(0.01)
        self.offset.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.offset.setProperty("value", 1.65)
        self.offset.setObjectName("offset")
        self.gridLayout.addWidget(self.offset, 3, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)
        self.btn = QtWidgets.QPushButton(Form)
        self.btn.setCheckable(True)
        self.btn.setObjectName("btn")
        self.gridLayout.addWidget(self.btn, 6, 0, 1, 2)
        self.delay = QtWidgets.QSpinBox(Form)
        self.delay.setAlignment(QtCore.Qt.AlignCenter)
        self.delay.setPrefix("")
        self.delay.setMinimum(100)
        self.delay.setMaximum(10000)
        self.delay.setSingleStep(100)
        self.delay.setProperty("value", 1500)
        self.delay.setDisplayIntegerBase(10)
        self.delay.setObjectName("delay")
        self.gridLayout.addWidget(self.delay, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.timeout = QtWidgets.QCheckBox(Form)
        self.timeout.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.timeout.setChecked(True)
        self.timeout.setObjectName("timeout")
        self.gridLayout.addWidget(self.timeout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "FunctionalGenerator"))
        self.amplitude.setSuffix(_translate("Form", " В"))
        self.label_8.setText(_translate("Form", "Скважность: "))
        self.period.setSuffix(_translate("Form", " мс"))
        self.offset.setSuffix(_translate("Form", " В"))
        self.label_7.setText(_translate("Form", "Смещение: "))
        self.label_9.setText(_translate("Form", "Период: "))
        self.btn.setText(_translate("Form", "Сигнал"))
        self.delay.setSuffix(_translate("Form", " мс"))
        self.label_6.setText(_translate("Form", "Амплитуда: "))
        self.timeout.setText(_translate("Form", "Длительность:"))