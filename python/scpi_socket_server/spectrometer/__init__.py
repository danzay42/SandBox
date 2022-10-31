import sys
import traceback
import logging

__all__ = [
	'run',
	'logger',
]
__version__ = '0.1.0'

if __debug__ is True:
	logger = logging.getLogger('debug')
else:
	logger = logging.getLogger('release')

	
from .core import Core


logger.info(f'__debug__={__debug__}')


def run():
	Core().exec()


def sys_excepthook(exc_type, exc_value, exc_traceback):
	if issubclass(exc_type, KeyboardInterrupt):
		logger.info("KeyboardInterrupt")
		sys.__excepthook__(exc_type, exc_value, exc_traceback)
	else:
		logger.fatal(str(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))))


sys.excepthook = sys_excepthook
