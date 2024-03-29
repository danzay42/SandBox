# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/daniil/Documents/TESART_Projects/CAFAR/ppm/ppm_module/ui/tm.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(488, 440)
        self.gridLayout_9 = QtWidgets.QGridLayout(Form)
        self.gridLayout_9.setContentsMargins(3, 3, 3, 3)
        self.gridLayout_9.setSpacing(3)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.widget_fan = QtWidgets.QWidget(Form)
        self.widget_fan.setObjectName("widget_fan")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_fan)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.temperature_current = QtWidgets.QSpinBox(self.widget_fan)
        self.temperature_current.setAlignment(QtCore.Qt.AlignCenter)
        self.temperature_current.setReadOnly(True)
        self.temperature_current.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.temperature_current.setMaximum(100)
        self.temperature_current.setProperty("value", 21)
        self.temperature_current.setObjectName("temperature_current")
        self.gridLayout_2.addWidget(self.temperature_current, 0, 0, 1, 1)
        self.btn_temp_update = QtWidgets.QPushButton(self.widget_fan)
        self.btn_temp_update.setCheckable(True)
        self.btn_temp_update.setObjectName("btn_temp_update")
        self.gridLayout_2.addWidget(self.btn_temp_update, 0, 1, 1, 1)
        self.temperature_auto = QtWidgets.QSpinBox(self.widget_fan)
        self.temperature_auto.setAlignment(QtCore.Qt.AlignCenter)
        self.temperature_auto.setMinimum(0)
        self.temperature_auto.setMaximum(100)
        self.temperature_auto.setProperty("value", 21)
        self.temperature_auto.setObjectName("temperature_auto")
        self.gridLayout_2.addWidget(self.temperature_auto, 1, 0, 1, 1)
        self.btn_temp_control = QtWidgets.QPushButton(self.widget_fan)
        self.btn_temp_control.setCheckable(True)
        self.btn_temp_control.setObjectName("btn_temp_control")
        self.gridLayout_2.addWidget(self.btn_temp_control, 1, 1, 1, 1)
        self.lable = QtWidgets.QLabel(self.widget_fan)
        self.lable.setAlignment(QtCore.Qt.AlignCenter)
        self.lable.setObjectName("lable")
        self.gridLayout_2.addWidget(self.lable, 2, 0, 1, 2)
        self.pwm_slider = QtWidgets.QSlider(self.widget_fan)
        self.pwm_slider.setMaximum(100)
        self.pwm_slider.setProperty("value", 50)
        self.pwm_slider.setOrientation(QtCore.Qt.Horizontal)
        self.pwm_slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.pwm_slider.setObjectName("pwm_slider")
        self.gridLayout_2.addWidget(self.pwm_slider, 3, 0, 1, 2)
        self.gridLayout_9.addWidget(self.widget_fan, 0, 0, 2, 1)
        self.widget_auto = QtWidgets.QWidget(Form)
        self.widget_auto.setMinimumSize(QtCore.QSize(240, 0))
        self.widget_auto.setObjectName("widget_auto")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.widget_auto)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setSpacing(3)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label = QtWidgets.QLabel(self.widget_auto)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_8.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget_auto)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_8.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget_auto)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout_8.addWidget(self.label_3, 2, 1, 1, 1)
        self.phs_box_0 = QtWidgets.QComboBox(self.widget_auto)
        self.phs_box_0.setObjectName("phs_box_0")
        self.gridLayout_8.addWidget(self.phs_box_0, 2, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget_auto)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout_8.addWidget(self.label_4, 2, 3, 1, 1)
        self.phs_box_1 = QtWidgets.QComboBox(self.widget_auto)
        self.phs_box_1.setObjectName("phs_box_1")
        self.gridLayout_8.addWidget(self.phs_box_1, 2, 4, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget_auto)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout_8.addWidget(self.label_5, 2, 5, 1, 1)
        self.phs_box_2 = QtWidgets.QComboBox(self.widget_auto)
        self.phs_box_2.setObjectName("phs_box_2")
        self.gridLayout_8.addWidget(self.phs_box_2, 2, 6, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget_auto)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.gridLayout_8.addWidget(self.label_6, 2, 7, 1, 1)
        self.phs_box_3 = QtWidgets.QComboBox(self.widget_auto)
        self.phs_box_3.setObjectName("phs_box_3")
        self.gridLayout_8.addWidget(self.phs_box_3, 2, 8, 1, 1)
        self.att_box = QtWidgets.QComboBox(self.widget_auto)
        self.att_box.setObjectName("att_box")
        self.gridLayout_8.addWidget(self.att_box, 1, 2, 1, 7)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ctrl13_rb = QtWidgets.QRadioButton(self.widget_auto)
        self.ctrl13_rb.setObjectName("ctrl13_rb")
        self.horizontalLayout_4.addWidget(self.ctrl13_rb)
        self.ctrl24_rb = QtWidgets.QRadioButton(self.widget_auto)
        self.ctrl24_rb.setObjectName("ctrl24_rb")
        self.horizontalLayout_4.addWidget(self.ctrl24_rb)
        self.tx_rb = QtWidgets.QRadioButton(self.widget_auto)
        self.tx_rb.setObjectName("tx_rb")
        self.horizontalLayout_4.addWidget(self.tx_rb)
        self.rx_rb = QtWidgets.QRadioButton(self.widget_auto)
        self.rx_rb.setObjectName("rx_rb")
        self.horizontalLayout_4.addWidget(self.rx_rb)
        self.gridLayout_8.addLayout(self.horizontalLayout_4, 0, 0, 1, 9)
        self.gridLayout_9.addWidget(self.widget_auto, 2, 0, 1, 2)
        self.widget_manual = QtWidgets.QWidget(Form)
        self.widget_manual.setObjectName("widget_manual")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_manual)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_13 = QtWidgets.QGroupBox(self.widget_manual)
        self.groupBox_13.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_13.setObjectName("groupBox_13")
        self.gg_2 = QtWidgets.QGridLayout(self.groupBox_13)
        self.gg_2.setContentsMargins(0, 0, 0, 0)
        self.gg_2.setSpacing(0)
        self.gg_2.setObjectName("gg_2")
        self.data_1_5 = QtWidgets.QCheckBox(self.groupBox_13)
        self.data_1_5.setObjectName("data_1_5")
        self.gg_2.addWidget(self.data_1_5, 0, 0, 1, 1)
        self.data_1_7 = QtWidgets.QCheckBox(self.groupBox_13)
        self.data_1_7.setObjectName("data_1_7")
        self.gg_2.addWidget(self.data_1_7, 0, 2, 1, 1)
        self.data_1_6 = QtWidgets.QCheckBox(self.groupBox_13)
        self.data_1_6.setObjectName("data_1_6")
        self.gg_2.addWidget(self.data_1_6, 0, 1, 1, 1)
        self.data_1_8 = QtWidgets.QCheckBox(self.groupBox_13)
        self.data_1_8.setObjectName("data_1_8")
        self.gg_2.addWidget(self.data_1_8, 0, 3, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_13, 0, 1, 1, 1)
        self.groupBox_11 = QtWidgets.QGroupBox(self.widget_manual)
        self.groupBox_11.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_11.setObjectName("groupBox_11")
        self._3 = QtWidgets.QGridLayout(self.groupBox_11)
        self._3.setContentsMargins(0, 0, 0, 0)
        self._3.setSpacing(0)
        self._3.setObjectName("_3")
        self.data_6_1 = QtWidgets.QCheckBox(self.groupBox_11)
        self.data_6_1.setObjectName("data_6_1")
        self._3.addWidget(self.data_6_1, 1, 1, 1, 1)
        self.data_6_2 = QtWidgets.QCheckBox(self.groupBox_11)
        self.data_6_2.setObjectName("data_6_2")
        self._3.addWidget(self.data_6_2, 1, 2, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox_11)
        self.label_15.setObjectName("label_15")
        self._3.addWidget(self.label_15, 0, 0, 1, 1)
        self.data_5_4 = QtWidgets.QCheckBox(self.groupBox_11)
        self.data_5_4.setObjectName("data_5_4")
        self._3.addWidget(self.data_5_4, 0, 4, 1, 1)
        self.data_5_3 = QtWidgets.QCheckBox(self.groupBox_11)
        self.data_5_3.setObjectName("data_5_3")
        self._3.addWidget(self.data_5_3, 0, 3, 1, 1)
        self.data_5_2 = QtWidgets.QCheckBox(self.groupBox_11)
        self.data_5_2.setObjectName("data_5_2")
        self._3.addWidget(self.data_5_2, 0, 2, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.groupBox_11)
        self.label_16.setObjectName("label_16")
        self._3.addWidget(self.label_16, 1, 0, 1, 1)
        self.data_5_1 = QtWidgets.QCheckBox(self.groupBox_11)
        self.data_5_1.setObjectName("data_5_1")
        self._3.addWidget(self.data_5_1, 0, 1, 1, 1)
        self.data_6_4 = QtWidgets.QCheckBox(self.groupBox_11)
        self.data_6_4.setObjectName("data_6_4")
        self._3.addWidget(self.data_6_4, 1, 4, 1, 1)
        self.data_6_3 = QtWidgets.QCheckBox(self.groupBox_11)
        self.data_6_3.setObjectName("data_6_3")
        self._3.addWidget(self.data_6_3, 1, 3, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_11, 1, 1, 1, 1)
        self.groupBox_12 = QtWidgets.QGroupBox(self.widget_manual)
        self.groupBox_12.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_12.setObjectName("groupBox_12")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_12)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.data_5_5 = QtWidgets.QCheckBox(self.groupBox_12)
        self.data_5_5.setObjectName("data_5_5")
        self.gridLayout_6.addWidget(self.data_5_5, 0, 0, 1, 1)
        self.data_5_6 = QtWidgets.QCheckBox(self.groupBox_12)
        self.data_5_6.setObjectName("data_5_6")
        self.gridLayout_6.addWidget(self.data_5_6, 0, 1, 1, 1)
        self.data_6_5 = QtWidgets.QCheckBox(self.groupBox_12)
        self.data_6_5.setObjectName("data_6_5")
        self.gridLayout_6.addWidget(self.data_6_5, 1, 0, 1, 1)
        self.data_6_6 = QtWidgets.QCheckBox(self.groupBox_12)
        self.data_6_6.setObjectName("data_6_6")
        self.gridLayout_6.addWidget(self.data_6_6, 1, 1, 1, 1)
        self.data_6_8 = QtWidgets.QCheckBox(self.groupBox_12)
        self.data_6_8.setObjectName("data_6_8")
        self.gridLayout_6.addWidget(self.data_6_8, 2, 1, 1, 1)
        self.data_6_7 = QtWidgets.QCheckBox(self.groupBox_12)
        self.data_6_7.setObjectName("data_6_7")
        self.gridLayout_6.addWidget(self.data_6_7, 2, 0, 1, 1)
        self.data_5_7 = QtWidgets.QCheckBox(self.groupBox_12)
        self.data_5_7.setObjectName("data_5_7")
        self.gridLayout_6.addWidget(self.data_5_7, 3, 0, 1, 1)
        self.data_5_8 = QtWidgets.QCheckBox(self.groupBox_12)
        self.data_5_8.setObjectName("data_5_8")
        self.gridLayout_6.addWidget(self.data_5_8, 3, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_12, 2, 1, 1, 1)
        self.groupBox_10 = QtWidgets.QGroupBox(self.widget_manual)
        self.groupBox_10.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_10.setObjectName("groupBox_10")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_10)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.data_3_5 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_3_5.setObjectName("data_3_5")
        self.gridLayout_5.addWidget(self.data_3_5, 3, 1, 1, 1)
        self.data_2_3 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_2_3.setObjectName("data_2_3")
        self.gridLayout_5.addWidget(self.data_2_3, 0, 3, 1, 1)
        self.data_3_1 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_3_1.setObjectName("data_3_1")
        self.gridLayout_5.addWidget(self.data_3_1, 2, 1, 1, 1)
        self.data_2_1 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_2_1.setObjectName("data_2_1")
        self.gridLayout_5.addWidget(self.data_2_1, 0, 1, 1, 1)
        self.data_3_7 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_3_7.setObjectName("data_3_7")
        self.gridLayout_5.addWidget(self.data_3_7, 3, 3, 1, 1)
        self.data_2_7 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_2_7.setObjectName("data_2_7")
        self.gridLayout_5.addWidget(self.data_2_7, 1, 3, 1, 1)
        self.data_2_4 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_2_4.setObjectName("data_2_4")
        self.gridLayout_5.addWidget(self.data_2_4, 0, 4, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox_10)
        self.label_11.setTextFormat(QtCore.Qt.PlainText)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_5.addWidget(self.label_11, 3, 0, 1, 1)
        self.data_2_2 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_2_2.setObjectName("data_2_2")
        self.gridLayout_5.addWidget(self.data_2_2, 0, 2, 1, 1)
        self.data_3_2 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_3_2.setObjectName("data_3_2")
        self.gridLayout_5.addWidget(self.data_3_2, 2, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox_10)
        self.label_12.setTextFormat(QtCore.Qt.PlainText)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_5.addWidget(self.label_12, 0, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox_10)
        self.label_14.setTextFormat(QtCore.Qt.PlainText)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_5.addWidget(self.label_14, 2, 0, 1, 1)
        self.data_2_8 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_2_8.setObjectName("data_2_8")
        self.gridLayout_5.addWidget(self.data_2_8, 1, 4, 1, 1)
        self.data_2_6 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_2_6.setObjectName("data_2_6")
        self.gridLayout_5.addWidget(self.data_2_6, 1, 2, 1, 1)
        self.data_3_4 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_3_4.setObjectName("data_3_4")
        self.gridLayout_5.addWidget(self.data_3_4, 2, 4, 1, 1)
        self.data_3_8 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_3_8.setObjectName("data_3_8")
        self.gridLayout_5.addWidget(self.data_3_8, 3, 4, 1, 1)
        self.data_3_6 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_3_6.setObjectName("data_3_6")
        self.gridLayout_5.addWidget(self.data_3_6, 3, 2, 1, 1)
        self.data_2_5 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_2_5.setObjectName("data_2_5")
        self.gridLayout_5.addWidget(self.data_2_5, 1, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox_10)
        self.label_13.setTextFormat(QtCore.Qt.PlainText)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_5.addWidget(self.label_13, 1, 0, 1, 1)
        self.data_3_3 = QtWidgets.QCheckBox(self.groupBox_10)
        self.data_3_3.setObjectName("data_3_3")
        self.gridLayout_5.addWidget(self.data_3_3, 2, 3, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_10, 2, 0, 1, 1)
        self.groupBox_14 = QtWidgets.QGroupBox(self.widget_manual)
        self.groupBox_14.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_14.setObjectName("groupBox_14")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_14)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.data_4_6 = QtWidgets.QCheckBox(self.groupBox_14)
        self.data_4_6.setObjectName("data_4_6")
        self.gridLayout_7.addWidget(self.data_4_6, 1, 2, 1, 1)
        self.data_4_3 = QtWidgets.QCheckBox(self.groupBox_14)
        self.data_4_3.setObjectName("data_4_3")
        self.gridLayout_7.addWidget(self.data_4_3, 0, 3, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.groupBox_14)
        self.label_18.setTextFormat(QtCore.Qt.PlainText)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.gridLayout_7.addWidget(self.label_18, 0, 0, 1, 1)
        self.data_4_2 = QtWidgets.QCheckBox(self.groupBox_14)
        self.data_4_2.setObjectName("data_4_2")
        self.gridLayout_7.addWidget(self.data_4_2, 0, 2, 1, 1)
        self.data_4_7 = QtWidgets.QCheckBox(self.groupBox_14)
        self.data_4_7.setObjectName("data_4_7")
        self.gridLayout_7.addWidget(self.data_4_7, 1, 3, 1, 2)
        self.data_4_1 = QtWidgets.QCheckBox(self.groupBox_14)
        self.data_4_1.setObjectName("data_4_1")
        self.gridLayout_7.addWidget(self.data_4_1, 0, 1, 1, 1)
        self.data_4_4 = QtWidgets.QCheckBox(self.groupBox_14)
        self.data_4_4.setObjectName("data_4_4")
        self.gridLayout_7.addWidget(self.data_4_4, 0, 4, 1, 1)
        self.data_4_5 = QtWidgets.QCheckBox(self.groupBox_14)
        self.data_4_5.setObjectName("data_4_5")
        self.gridLayout_7.addWidget(self.data_4_5, 1, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.groupBox_14)
        self.label_17.setTextFormat(QtCore.Qt.PlainText)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout_7.addWidget(self.label_17, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_14, 0, 0, 2, 1)
        self.gridLayout_9.addWidget(self.widget_manual, 3, 0, 1, 2)
        self.widget_dut = QtWidgets.QWidget(Form)
        self.widget_dut.setObjectName("widget_dut")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_dut)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(self.widget_dut)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.widget_address = QtWidgets.QSpinBox(self.widget_dut)
        self.widget_address.setAlignment(QtCore.Qt.AlignCenter)
        self.widget_address.setMaximum(63)
        self.widget_address.setObjectName("widget_address")
        self.gridLayout.addWidget(self.widget_address, 0, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.widget_dut)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.widget_state = QtWidgets.QWidget(self.widget_dut)
        self.widget_state.setObjectName("widget_state")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_state)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.status = QtWidgets.QLabel(self.widget_state)
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setObjectName("status")
        self.horizontalLayout.addWidget(self.status)
        self.btn_read = QtWidgets.QPushButton(self.widget_state)
        self.btn_read.setMinimumSize(QtCore.QSize(100, 0))
        self.btn_read.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_read.setObjectName("btn_read")
        self.horizontalLayout.addWidget(self.btn_read)
        self.gridLayout.addWidget(self.widget_state, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget_dut)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.widget_load = QtWidgets.QWidget(self.widget_dut)
        self.widget_load.setObjectName("widget_load")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_load)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.data_1_1 = QtWidgets.QCheckBox(self.widget_load)
        self.data_1_1.setObjectName("data_1_1")
        self.horizontalLayout_3.addWidget(self.data_1_1)
        self.data_1_2 = QtWidgets.QCheckBox(self.widget_load)
        self.data_1_2.setObjectName("data_1_2")
        self.horizontalLayout_3.addWidget(self.data_1_2)
        self.btn_write = QtWidgets.QPushButton(self.widget_load)
        self.btn_write.setMinimumSize(QtCore.QSize(100, 0))
        self.btn_write.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_write.setObjectName("btn_write")
        self.horizontalLayout_3.addWidget(self.btn_write)
        self.gridLayout.addWidget(self.widget_load, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.widget_dut)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
        self.widget_set = QtWidgets.QWidget(self.widget_dut)
        self.widget_set.setObjectName("widget_set")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_set)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_sel_0 = QtWidgets.QRadioButton(self.widget_set)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_sel_0.sizePolicy().hasHeightForWidth())
        self.btn_sel_0.setSizePolicy(sizePolicy)
        self.btn_sel_0.setObjectName("btn_sel_0")
        self.horizontalLayout_2.addWidget(self.btn_sel_0)
        self.btn_sel_1 = QtWidgets.QRadioButton(self.widget_set)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_sel_1.sizePolicy().hasHeightForWidth())
        self.btn_sel_1.setSizePolicy(sizePolicy)
        self.btn_sel_1.setObjectName("btn_sel_1")
        self.horizontalLayout_2.addWidget(self.btn_sel_1)
        self.btn_sel_2 = QtWidgets.QRadioButton(self.widget_set)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_sel_2.sizePolicy().hasHeightForWidth())
        self.btn_sel_2.setSizePolicy(sizePolicy)
        self.btn_sel_2.setObjectName("btn_sel_2")
        self.horizontalLayout_2.addWidget(self.btn_sel_2)
        self.gridLayout.addWidget(self.widget_set, 3, 1, 1, 1)
        self.gridLayout_9.addWidget(self.widget_dut, 0, 1, 2, 1)

        self.retranslateUi(Form)
        self.btn_temp_control.toggled['bool'].connect(self.btn_temp_update.setChecked) # type: ignore
        self.tx_rb.toggled['bool'].connect(self.data_1_5.setChecked) # type: ignore
        self.tx_rb.toggled['bool'].connect(self.data_1_6.setChecked) # type: ignore
        self.tx_rb.toggled['bool'].connect(self.data_1_7.setChecked) # type: ignore
        self.tx_rb.toggled['bool'].connect(self.data_1_8.setChecked) # type: ignore
        self.rx_rb.toggled['bool'].connect(self.data_6_1.setChecked) # type: ignore
        self.rx_rb.toggled['bool'].connect(self.data_6_2.setChecked) # type: ignore
        self.rx_rb.toggled['bool'].connect(self.data_6_3.setChecked) # type: ignore
        self.rx_rb.toggled['bool'].connect(self.data_6_4.setChecked) # type: ignore
        self.rx_rb.toggled['bool'].connect(self.data_5_5.setChecked) # type: ignore
        self.rx_rb.toggled['bool'].connect(self.data_6_5.setChecked) # type: ignore
        self.rx_rb.toggled['bool'].connect(self.data_6_7.setChecked) # type: ignore
        self.rx_rb.toggled['bool'].connect(self.data_5_6.setChecked) # type: ignore
        self.rx_rb.toggled['bool'].connect(self.data_6_6.setChecked) # type: ignore
        self.rx_rb.toggled['bool'].connect(self.data_6_8.setChecked) # type: ignore
        self.rx_rb.toggled['bool'].connect(self.data_5_8.setChecked) # type: ignore
        self.ctrl13_rb.toggled['bool'].connect(self.data_5_1.setChecked) # type: ignore
        self.ctrl13_rb.toggled['bool'].connect(self.data_5_3.setChecked) # type: ignore
        self.ctrl13_rb.toggled['bool'].connect(self.data_5_5.setChecked) # type: ignore
        self.ctrl13_rb.toggled['bool'].connect(self.data_5_6.setChecked) # type: ignore
        self.ctrl13_rb.toggled['bool'].connect(self.data_6_6.setChecked) # type: ignore
        self.ctrl13_rb.toggled['bool'].connect(self.data_5_8.setChecked) # type: ignore
        self.ctrl13_rb.toggled['bool'].connect(self.data_6_8.setChecked) # type: ignore
        self.ctrl24_rb.toggled['bool'].connect(self.data_5_2.setChecked) # type: ignore
        self.ctrl24_rb.toggled['bool'].connect(self.data_5_4.setChecked) # type: ignore
        self.ctrl24_rb.toggled['bool'].connect(self.data_5_5.setChecked) # type: ignore
        self.ctrl24_rb.toggled['bool'].connect(self.data_5_6.setChecked) # type: ignore
        self.ctrl24_rb.toggled['bool'].connect(self.data_6_5.setChecked) # type: ignore
        self.ctrl24_rb.toggled['bool'].connect(self.data_6_7.setChecked) # type: ignore
        self.ctrl24_rb.toggled['bool'].connect(self.data_5_8.setChecked) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "TransceiverModule"))
        self.temperature_current.setSuffix(_translate("Form", "°C"))
        self.btn_temp_update.setText(_translate("Form", "Текущая:"))
        self.temperature_auto.setSuffix(_translate("Form", "°C"))
        self.btn_temp_control.setText(_translate("Form", "АвтоКонроль:"))
        self.lable.setText(_translate("Form", "ШИМ вентилятора:"))
        self.label.setText(_translate("Form", "Атт (dB): "))
        self.label_2.setText(_translate("Form", "Фаза (°): "))
        self.label_3.setText(_translate("Form", "1:"))
        self.label_4.setText(_translate("Form", "2:"))
        self.label_5.setText(_translate("Form", "3:"))
        self.label_6.setText(_translate("Form", "4:"))
        self.ctrl13_rb.setText(_translate("Form", "Контр_13"))
        self.ctrl24_rb.setText(_translate("Form", "Контр_24"))
        self.tx_rb.setText(_translate("Form", "Tx"))
        self.rx_rb.setText(_translate("Form", "Rx"))
        self.groupBox_13.setTitle(_translate("Form", "SW_IZ"))
        self.data_1_5.setText(_translate("Form", "1"))
        self.data_1_7.setText(_translate("Form", "3"))
        self.data_1_6.setText(_translate("Form", "2"))
        self.data_1_8.setText(_translate("Form", "4"))
        self.groupBox_11.setTitle(_translate("Form", "SW_KEY"))
        self.data_6_1.setText(_translate("Form", "1"))
        self.data_6_2.setText(_translate("Form", "2"))
        self.label_15.setText(_translate("Form", "TXC:"))
        self.data_5_4.setText(_translate("Form", "4"))
        self.data_5_3.setText(_translate("Form", "3"))
        self.data_5_2.setText(_translate("Form", "2"))
        self.label_16.setText(_translate("Form", "RXC:"))
        self.data_5_1.setText(_translate("Form", "1"))
        self.data_6_4.setText(_translate("Form", "4"))
        self.data_6_3.setText(_translate("Form", "3"))
        self.groupBox_12.setTitle(_translate("Form", "SW"))
        self.data_5_5.setText(_translate("Form", "TXE_1"))
        self.data_5_6.setText(_translate("Form", "TXE_2"))
        self.data_6_5.setText(_translate("Form", "COM_1"))
        self.data_6_6.setText(_translate("Form", "COM_2"))
        self.data_6_8.setText(_translate("Form", "ENT_2"))
        self.data_6_7.setText(_translate("Form", "ENT_1"))
        self.data_5_7.setText(_translate("Form", "TXRX"))
        self.data_5_8.setText(_translate("Form", "RXE"))
        self.groupBox_10.setTitle(_translate("Form", "Phase"))
        self.data_3_5.setText(_translate("Form", "22.5°"))
        self.data_2_3.setText(_translate("Form", "90°"))
        self.data_3_1.setText(_translate("Form", "22.5°"))
        self.data_2_1.setText(_translate("Form", "22.5°"))
        self.data_3_7.setText(_translate("Form", "90°"))
        self.data_2_7.setText(_translate("Form", "90°"))
        self.data_2_4.setText(_translate("Form", "180°"))
        self.label_11.setText(_translate("Form", "4:"))
        self.data_2_2.setText(_translate("Form", "45°"))
        self.data_3_2.setText(_translate("Form", "45°"))
        self.label_12.setText(_translate("Form", "1:"))
        self.label_14.setText(_translate("Form", "3:"))
        self.data_2_8.setText(_translate("Form", "180°"))
        self.data_2_6.setText(_translate("Form", "45°"))
        self.data_3_4.setText(_translate("Form", "180°"))
        self.data_3_8.setText(_translate("Form", "180°"))
        self.data_3_6.setText(_translate("Form", "45°"))
        self.data_2_5.setText(_translate("Form", "22.5°"))
        self.label_13.setText(_translate("Form", "2:"))
        self.data_3_3.setText(_translate("Form", "90°"))
        self.groupBox_14.setTitle(_translate("Form", "Attenuation"))
        self.data_4_6.setText(_translate("Form", "8dB"))
        self.data_4_3.setText(_translate("Form", "Ch3"))
        self.label_18.setText(_translate("Form", "2db:"))
        self.data_4_2.setText(_translate("Form", "Ch2"))
        self.data_4_7.setText(_translate("Form", "16dB"))
        self.data_4_1.setText(_translate("Form", "Ch1"))
        self.data_4_4.setText(_translate("Form", "Ch4"))
        self.data_4_5.setText(_translate("Form", "4dB"))
        self.label_17.setText(_translate("Form", "all:"))
        self.label_7.setText(_translate("Form", "Адрес:"))
        self.label_10.setText(_translate("Form", "Read:"))
        self.status.setText(_translate("Form", "0b________"))
        self.btn_read.setText(_translate("Form", "Читать"))
        self.label_8.setText(_translate("Form", "Write:"))
        self.data_1_1.setText(_translate("Form", "0х1"))
        self.data_1_2.setText(_translate("Form", "0х2"))
        self.btn_write.setText(_translate("Form", "Записать"))
        self.label_9.setText(_translate("Form", "Select:"))
        self.btn_sel_0.setText(_translate("Form", "0х0"))
        self.btn_sel_1.setText(_translate("Form", "0х1"))
        self.btn_sel_2.setText(_translate("Form", "0х2"))
