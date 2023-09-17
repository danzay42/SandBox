from ppm_module.devices.power_source import PowerSource
from ppm_module.devices.functional_generator import FunctionalGenerator
from ppm_module.devices.source_measure_unit import SourceMeasureUnit, SourceMeasureUnit1, SourceMeasureUnit2
from ppm_module.devices.fpga_max import TransceiverModule
from ppm_module.devices.vector_network_analyzer import VectorNetworkAnalyzer
from ppm_module.devices.spectrum_analyzer import SpectrumAnalyzer
from ppm_module.pyqt_instruments import ui_data_saver
from ppm_module.ui.main_window import Ui_MainWindow, QtCore, QtGui, QtWidgets
import ppm_module.scpi_cmds.instruction_parser as scpi
from ppm_module import logger

import time
import sys
import traceback
import subprocess


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	Q_APP = QtWidgets.QApplication(sys.argv)
	TM: TransceiverModule
	PS: PowerSource
	FG: FunctionalGenerator
	SMU_1: SourceMeasureUnit
	SMU_2: SourceMeasureUnit
	VNA: VectorNetworkAnalyzer
	SA: SpectrumAnalyzer
	StepGenerator = None
	
	def __init__(self):
		sys.excepthook = self.except_hook
		super(MainWindow, self).__init__()
		dev_addresses = scpi.get_json_dict(scpi.config)
		self.PS = PowerSource(parent=self, addr=dev_addresses[scpi.default_ps])
		self.FG = FunctionalGenerator(parent=self, addr=dev_addresses[scpi.default_fg])
		self.SMU_1 = SourceMeasureUnit1(parent=self, addr=dev_addresses[scpi.default_smu_1])
		self.SMU_2 = SourceMeasureUnit2(parent=self, addr=dev_addresses[scpi.default_smu_2])
		self.VNA = VectorNetworkAnalyzer(parent=self, addr=dev_addresses[scpi.default_vna])
		self.SA = SpectrumAnalyzer(parent=self, addr=dev_addresses[scpi.default_sa])
		self.TM = TransceiverModule(parent=self)
		self.DEVS = [self.TM, self.VNA, self.SA, self.PS, self.FG, self.SMU_1, self.SMU_2]
		self.setupUi(self)
		self.signals_connection()
		self.show()
		self.FUNC = TaskFunctions(self)
	
	def exec(self) -> int:
		return self.Q_APP.exec_()
	
	def except_hook(self, exc_type, exc_value, exc_traceback):
		if issubclass(exc_type, KeyboardInterrupt):
			sys.__excepthook__(exc_type, exc_value, exc_traceback)
		else:
			logger.ERROR(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
			QtWidgets.QMessageBox.warning(self, exc_value.__class__.__name__, str(exc_value))
	
	def setupUi(self, window):
		super(MainWindow, self).setupUi(window)
		self._setup_ui_dock_widgets()
		self._setup_ui_technics()
		self.load()
	
	def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
		self.save()
		for dev in self.DEVS:
			if dev.used:
				dev.device.rst()
	
	def signals_connection(self):
		self.task_list.currentIndexChanged.connect(lambda i: self.info.setPlainText(self.task_list.itemData(i)))
		self.run.clicked.connect(self.create_step_generator)
		self.pic.installEventFilter(self)
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.next_step)
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.previous_step)
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).clicked.connect(
			lambda a: self._setup_ui_technics_state(False))
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(
			lambda a: self._setup_ui_technics_state(False))

	def _setup_ui_dock_widgets(self):
		docks = [self.dockWidget]
		for dev in self.DEVS:
			dock = QtWidgets.QDockWidget(dev.state_label.text(), self)
			dock.setWidget(dev)
			dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetMovable)
			docks.append(dock)
			item = QtWidgets.QListWidgetItem()
			self.listWidget.addItem(item)
			self.listWidget.setItemWidget(item, dev.state_label)
			self.tabifyDockWidget(self.dockWidget, dock)
		self.listWidget.currentRowChanged.connect(lambda var: docks[var].raise_())
		self.dockWidget.raise_()
	
	def _setup_ui_technics(self):
		for item in scpi.get_json_dict(scpi.technics):
			self.task_list.addItem(f"{item[scpi.num]}. {item[scpi.title]}", item.get(scpi.description, ''))
		self.info.setPlainText(self.task_list.currentData())
		
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).setText("Сбросить и Выйти")
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).setText("Далее")
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).setText("Назад")
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("Завершить")
		self._setup_ui_technics_state(False)
	
	def _setup_ui_technics_state(self, state):
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).setVisible(state)
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).setVisible(state)
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).setVisible(state)
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setVisible(state)
		self.pic.setVisible(state)
		self.label.setVisible(state)
		self.info.clear()
		self.info.setPlainText(self.task_list.itemData(self.task_list.currentIndex()))
		self.task_list.setEnabled(not state)
		self.run.setEnabled(not state)

	def setup_ui_technics_block(self, state):
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).setEnabled(not state)
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).setEnabled(not state)
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).setEnabled(not state)
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(not state)
	
	def eventFilter(self, target: QtCore.QObject, event: QtCore.QEvent) -> bool:
		if target == self.pic and event.type() == QtCore.QEvent.MouseButtonDblClick:
			path = getattr(self.pic, 'data', None)
			if path:
				self.open_image(path)
		return False
	
	@staticmethod
	def open_image(path):
		cmd = {'linux': 'xdg-open',
		       'win32': 'explorer',
		       'darwin': 'open'}[sys.platform]
		subprocess.run([cmd, path])
	
	def save(self):
		settings = QtCore.QSettings("config.ini", QtCore.QSettings.Format.IniFormat)
		ui_data_saver.save_windows_values(settings, self)
		ui_data_saver.save_widgets_values(settings, self)
		ui_data_saver.save_tree(settings, self)

	def load(self):
		settings = QtCore.QSettings("config.ini", QtCore.QSettings.Format.IniFormat)
		ui_data_saver.restore_windows_values(settings, self)
		ui_data_saver.restore_widgets_values(settings, self)
		ui_data_saver.restore_tree(settings, self)
		
	def create_step_generator(self):
		self.StepGenerator = self.step_generator(self.task_list.currentIndex())
		next(self.StepGenerator)
		
	def step_generator(self, technique):
		json_data = scpi.get_json_dict(scpi.technics)[technique]
		step = 0
		while step < len(json_data[scpi.steps]):
			self.gui_step_update(json_data, step)
			args = self.parse_data(json_data, step)
			next_step = yield
			if next_step > 0:
				self.setup_ui_technics_block(True)
				text_info = self.FUNC.technique_function(*args)
				self.setup_ui_technics_block(False)
				if text_info:
					self.info.appendPlainText(text_info + '\n')
					self.info.moveCursor(QtGui.QTextCursor.End)
			step += next_step
	
	def parse_data(self, json_data, step):
		step_node = json_data[scpi.steps][step]
		action = step_node.get(scpi.action) or json_data.get(scpi.action)
		action_args = step_node.get(scpi.action_args) or json_data.get(scpi.action_args)
		timeout = step_node.get(scpi.acquire_timeout) or json_data.get(scpi.acquire_timeout)
		file = step_node.get(scpi.file) or json_data.get(scpi.file)
		cmds = scpi.parse_scpi_file(file)
		cmd_range = step_node.get(scpi.cmd_range)
		if cmds and cmd_range:
			from_, to_ = cmd_range
			cmds = cmds[from_: to_]
		return action, action_args, cmds, timeout
	
	def gui_step_update(self, json_data, step):
		step_node = json_data[scpi.steps][step]
		if step_node.get(scpi.description):
			self.info.appendPlainText('\n->' + step_node[scpi.description])
			self.info.moveCursor(QtGui.QTextCursor.End)
		label = step_node.get(scpi.label)
		if label:
			self.label.setText(label)
		self.label.setVisible(bool(label))
		pic = step_node.get(scpi.pic) or json_data.get(scpi.pic)
		if pic:
			self.pic.setPixmap(QtGui.QPixmap(
				scpi.folder_path + pic).scaled(
				400, 300, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
			self.pic.data = scpi.folder_path + pic
		self.pic.setVisible(bool(pic))
		
		if step == 1:
			self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).show()
		elif step == 0:
			self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).show()
			self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).hide()
			self.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).show()
			self.task_list.setEnabled(False)
			self.run.setEnabled(False)
	
	def next_step(self):
		try:
			self.StepGenerator.send(+1)
		except StopIteration:
			self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).hide()
			self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).hide()
			self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).show()
	
	def previous_step(self):
		self.StepGenerator.send(-1)


class TaskFunctions:
	parent: MainWindow
	
	def __init__(self, parent):
		self.parent = parent
	
	def technique_function(self, action, action_args, cmds, timeout):
		print(action, action_args, cmds, timeout)
		return ''

	def wizard_action(self, action, cmds, args, timeout, wizard):
		function = getattr(self, action) if action else self.action_vna
		return function(cmds, args, wizard, timeout)
	
	def action_8v_supply(self, *args):
		# self.parent.PS.btn_1.setChecked(True)
		# self.parent.PS.btn_2.setChecked(True)
		# self.parent.PS.btn_3.setChecked(True)
		# self.parent.PS.btn_4.setChecked(True)
		# self.parent.PS.btn_power.setChecked(True)
		self.parent.FG.set_settings()
		self.parent.TM.device.pulse()
		self.parent.FG.run(True)
	
	def action_get_current(self, *args):
		self.parent.PS.btn_1.setChecked(True)
		self.parent.PS.btn_2.setChecked(False)
		self.parent.PS.btn_3.setChecked(True)
		self.parent.PS.btn_4.setChecked(True)
		self.parent.PS.btn_power.setChecked(True)
		time.sleep(0.1)
		res = f"Канал 1:{self.parent.PS.gc_1.value()}mА {self.parent.PS.gv_1.value()}В" \
		      f"Канал 2:{self.parent.PS.gc_2.value()}mА {self.parent.PS.gv_2.value()}В" \
		      f"Канал 3:{self.parent.PS.gc_3.value()}mА {self.parent.PS.gv_3.value()}В" \
		      f"Канал 4:{self.parent.PS.gc_4.value()}mА {self.parent.PS.gv_4.value()}В"
		time.sleep(0.1)
		res += '\n'
		res += f"Канал 1:{self.parent.PS.gc_1.value()}mА {self.parent.PS.gv_1.value()}В" \
		       f"Канал 2:{self.parent.PS.gc_2.value()}mА {self.parent.PS.gv_2.value()}В" \
		       f"Канал 3:{self.parent.PS.gc_3.value()}mА {self.parent.PS.gv_3.value()}В" \
		       f"Канал 4:{self.parent.PS.gc_4.value()}mА {self.parent.PS.gv_4.value()}В"
		time.sleep(0.1)
		res += '\n'
		res += f"Канал 1:{self.parent.PS.gc_1.value()}mА {self.parent.PS.gv_1.value()}В" \
		       f"Канал 2:{self.parent.PS.gc_2.value()}mА {self.parent.PS.gv_2.value()}В" \
		       f"Канал 3:{self.parent.PS.gc_3.value()}mА {self.parent.PS.gv_3.value()}В" \
		       f"Канал 4:{self.parent.PS.gc_4.value()}mА {self.parent.PS.gv_4.value()}В"
		return res
	
	def action_waiter(self, cmds, args, wizard, timeout):
		cond_cmd, res_cmd = args
		for cmd in cmds:
			if cmd.strip() == cond_cmd:
				t_start = time.time()
				while time.time() - t_start < timeout and res_cmd != self.VNA.device.parse_scpi_cmd(cmd):
					time.sleep(0.5)
				continue
			self.parent.VNA.device.parse_scpi_cmd(cmd)
		return ''
	
	def action_phase(self, cmds, arguments, *args):
		self.parent.SMU_2.btn_1.setChecked(False)
		self.parent.SMU_2.btn_2.setChecked(False)
		for i in arguments:
			getattr(self.parent.SMU_2, f'btn_{i}').setChecked(True)
		return ''
	
	def action_sa(self, cmds, *args):
		_, _, timeout = args
		return ''.join([self.parent.SA.device.parse_scpi_cmd(cmd) for cmd in cmds])
	
	def action_vna(self, cmds, *args):
		_, _, timeout = args
		res = ''
		for cmd in cmds:
			res += self.parent.VNA.device.parse_scpi_cmd(cmd, timeout if scpi.acquire in cmd else None)
		return res


def run_console():
	app = MainWindow()
	app.exec()
	# input("Press Enter to exit...")


if __name__ == '__main__':
	run_console()
