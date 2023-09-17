

class CoreExceptions(Exception):
	code = 0
	description = "Base Core Exception"
	info = ""

	def __init__(self, info):
		self.info = info
		super(CoreExceptions, self).__init__()

	def __str__(self):
		return f"[-{self.code}]{self.description}: {self.info}"

	def __repr__(self):
		return f"[-{self.code}]{self.description}: {self.info}"


class TransportError(CoreExceptions):
	description = "Connection Exception"
	code = 1


class LogicError(CoreExceptions):
	description = "Script Exception"
	code = 2


class DeviceError(CoreExceptions):
	description = "Device Exception"
	code = 3
