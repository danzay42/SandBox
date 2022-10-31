import traceback
from . import logger


class NoError(Exception):
	code = 0
	description = 'NoError'

	def __init__(self, *args, exception: Exception = None):
		super(NoError, self).__init__(*args)
		if exception:
			msg = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
			logger.info(msg)

	def __repr__(self):
		return f"+{self.code}, {self.description}"


class WrongCommand(NoError):
	code = 1
	description = 'Wrong Command'


class WrongParameter(NoError):
	code = 2
	description = 'Wrong Parameter'


class ParameterOutOfRange(NoError):
	code = 3
	description = 'Parameter Out Of Range'


class Timeout(NoError):
	code = 4
	description = 'Data Await Timeout'
