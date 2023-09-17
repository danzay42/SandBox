from typing import List, Tuple
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QMainWindow, QSpinBox, QDoubleSpinBox,\
	QComboBox, QCheckBox, QRadioButton, QLineEdit, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import QSettings, QObject


__all__ = ["saved_widgets", "save_tree", "restore_tree",
           "save_windows_values", "restore_windows_values",
           "save_widgets_values", "restore_widgets_values"]

saved_widgets = (QCheckBox, QComboBox, QSpinBox, QDoubleSpinBox, QRadioButton, QLineEdit)

__widgets_properties = {
	QComboBox.staticMetaObject.className():
		(str, QComboBox.setCurrentText, QComboBox.currentText),
	QSpinBox.staticMetaObject.className():
		(int, QSpinBox.setValue, QSpinBox.value),
	QDoubleSpinBox.staticMetaObject.className():
		(float, QDoubleSpinBox.setValue, QDoubleSpinBox.value),
	QCheckBox.staticMetaObject.className():
		(bool, QCheckBox.setChecked, QCheckBox.isChecked),
	QLineEdit.staticMetaObject.className():
		(str, QLineEdit.setText, QLineEdit.text),
	QRadioButton.staticMetaObject.className():
		(bool, QRadioButton.setChecked, QRadioButton.isChecked),
}


def __find_widgets(main_widget: QWidget, types: Tuple[QWidget, ...]):
	return [w for w in main_widget.findChildren(types)
	        if w.objectName() and not w.objectName().startswith('qt_')]


def save_widgets_values(settings: QSettings, parent_widget: QWidget, types: Tuple[QWidget, ...] = saved_widgets):
	settings.beginGroup("Qt_Widgets")
	for widget in __find_widgets(parent_widget, types):
		_, _, get_ = __widgets_properties[widget.staticMetaObject.className()]
		settings.setValue(widget.objectName(), get_(widget))
	settings.endGroup()
	

def restore_widgets_values(settings: QSettings, parent_widget: QWidget, types: Tuple[QWidget, ...] = saved_widgets):
	settings.beginGroup("Qt_Widgets")
	for widget in __find_widgets(parent_widget, types):
		stored_value = settings.value(widget.objectName(), None)
		if stored_value is not None:
			type_, set_function_, _ = __widgets_properties[widget.staticMetaObject.className()]
			set_function_(widget, settings.value(widget.objectName(), type=type_))
	settings.endGroup()


def save_windows_values(settings: QSettings, *windows: QMainWindow):
	settings.beginGroup("Qt_Windows")
	for window in windows:
		settings.setValue(window.objectName() + "_size", window.size())
		settings.setValue(window.objectName() + "_pos", window.pos())
	settings.endGroup()


def restore_windows_values(settings: QSettings, *windows: QMainWindow):
	settings.beginGroup("Qt_Windows")
	for window in windows:
		window.resize(settings.value(window.objectName() + "_size", window.baseSize()))
		window.move(settings.value(window.objectName() + "_pos", window.pos()))
	settings.endGroup()


def __parameter_bypass(settings: QSettings, item: QTreeWidgetItem, depth_current, prefix_root, save=True):
	if item.childCount() and depth_current > 0:
		if save:
			settings.setValue(prefix_root, item.isExpanded())
		else:
			item.setExpanded(settings.value(prefix_root, True, bool))
		settings.beginGroup(prefix_root)
		for child in range(item.childCount()):
			__parameter_bypass(settings, item.child(child), depth_current - 1, str(child), save)
		settings.endGroup()


def __parameter_bypass_top(settings: QSettings, parent_widget: QWidget, depth=2, save=True):
	settings.beginGroup("Qt_Tree")
	for i, tree in enumerate(parent_widget.findChildren(QTreeWidget)):
		tree: QTreeWidget
		settings.beginGroup(tree.objectName())
		for item_i in range(tree.topLevelItemCount()):
			__parameter_bypass(settings, tree.topLevelItem(item_i), depth, str(item_i), save)
		settings.endGroup()
	settings.endGroup()


def save_tree(settings: QSettings, parent_widget: QWidget, depth=2):
	__parameter_bypass_top(settings, parent_widget, depth, save=True)


def restore_tree(settings: QSettings, parent_widget: QWidget, depth=2):
	__parameter_bypass_top(settings, parent_widget, depth, save=False)
