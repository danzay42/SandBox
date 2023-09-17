if __debug__ is True:
	from ppm_module.pyqt_instruments.ui_converter import convert
	from ppm_module import ui
	convert(ui)

import logging
logger = logging.getLogger('dev')

from ppm_module.core import run_console


__all__ = [
	"run_console",
	"logger"
	]


__version__ = '0.1.0'
