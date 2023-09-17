from . import logger, exceptions, visa


class SCPITransport:
	instr: visa.resources.MessageBasedResource | visa.Resource

	def __init__(self, addr, **kwarg):
		rm = visa.ResourceManager(kwarg.get("ResourceManager", "@py"))
		self.init_params = kwarg
		try:
			self.instr = rm.open_resource(addr)
		except visa.Error as e:
			raise exceptions.TransportError(str(e))
		if timeout := kwarg.get("timeout"):
			self.instr.timeout = timeout
		if term := kwarg.get("termination"):
			self.instr.read_termination = self.instr.write_termination = term
		if term_rd := kwarg.get("read_termination"):
			self.instr.read_termination = term_rd
		if term_wr := kwarg.get("write_termination"):
			self.instr.write_termination = term_wr
		self.instr.clear()
		logger.debug(f"{self.instr.resource_name} connect: {kwarg}")

	def write(self, cmd, log_debug=True):
		log = f"{self.instr.resource_name} write: {cmd}"
		logger.debug(log) if log_debug else logger.info(log)
		try:
			return self.instr.write(cmd)
		except visa.Error as e:
			raise exceptions.TransportError(str(e))

	def read(self, timeout=None, log_debug=True):
		try:
			if timeout:
				self.instr.timeout = timeout
				res = self.instr.read()
				self.instr.timeout = 2000
			else:
				res = self.instr.read()

			log = f"{self.instr.resource_name} read: {res}"
			logger.debug(log) if log_debug else logger.info(log)
			return res
		except visa.Error as e:
			raise exceptions.TransportError(str(e))

	def query(self, cmd, timeout=None, log_debug=True):
		self.write(cmd=cmd, log_debug=log_debug)
		return self.read(timeout=timeout, log_debug=log_debug)

	def send(self, cmd: str, timeout=None, log_debug=True):
		self.write(cmd=cmd, log_debug=log_debug)
		if "?" in cmd:
			return self.read(timeout=timeout, log_debug=log_debug)

	def send_err(self, cmd, timeout=None, log_debug=True):
		res = self.send(cmd, timeout=timeout, log_debug=log_debug)
		err = self.send(":SYST:ERR?", log_debug=log_debug)
		if "No error" not in err:
			logger.error(f"{self.instr.resource_name}: {cmd} -> {err}")
			raise exceptions.DeviceError(f"{self.instr.resource_name}: {cmd} -> {err}")
		return res

	def send_opc(self, cmd, timeout=None, log_debug=True):
		return self.send(f"*OPC;{cmd};*OPC?", timeout=timeout, log_debug=log_debug)

	def send_err_opc(self, cmd, timeout=None, log_debug=True):
		return self.send_err(f"*OPC;{cmd};*OPC?", timeout=timeout, log_debug=log_debug)


