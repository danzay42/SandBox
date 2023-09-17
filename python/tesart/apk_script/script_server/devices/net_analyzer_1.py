import asyncio
from . import logger, exceptions, visa, base


class NetAnalyzer(base.NetAnalyzer):
	channels: dict
	freq_trace: list[str]

	def __init__(self, **kwargs):
		super(NetAnalyzer, self).__init__(termination='\n', **kwargs)
		self.transport.send_err_opc("*CLS")
		self.transport.send_err_opc("*RST")

		self.transport.send_err_opc(':SYSTem:FPReset')
		self.transport.send_err_opc(':DISPlay:WINDow1:STATe 1')
		self.transport.send_err_opc(':CALCulate:PARameter:DELete:ALL')

		self.config_channels(**kwargs)

		# self.transport.send_err_opc(':FORMat:BORDer SWAPped')
		# self.transport.send_err_opc(':FORMat:DATA REAL,32')
		self.transport.send_err_opc(':FORMat:DATA ASCII,0')

	def info(self, *args, **kwargs):
		return self.transport.query("*IDN?")

	def config_channels(self, **kwargs):
		self.config_receive(**kwargs)
		self.config_transmit(**kwargs)

		channels = kwargs.get("channels", 1)
		traces = kwargs.get("traces", 1)

		self.channels = {ch+1: [ch*traces+(tr+1) for tr in range(traces)] for ch in range(channels)}

		for channel in list(self.channels.keys())[1:]:
			self.transport.send_err_opc(f':SYSTem:MACRo:COPY:CHANnel{1}:STATe {channel},-1,"state"')

		if path := kwargs.get("de-embedding"):
			for ch in self.channels:
				self.transport.send_err_opc(f':CALCulate{ch}:FSIMulator:SENDed:DEEMbed:PORT1:TYPE USER')
				self.transport.send_err_opc(
					f':CALCulate{ch}:FSIMulator:SENDed:DEEMbed:PORT1:USER:FILename "{path}/{ch}.s2p"')
				self.transport.send_err_opc(f':CALCulate{ch}:FSIMulator:SENDed:DEEMbed:STATe 1')
				self.transport.send_err_opc(f':CALCulate{ch}:FSIMulator:STATe 1')

		freq_start = float(self.transport.send(f':SENS:FREQ:STAR?').lstrip('+'))
		freq_stop = float(self.transport.send(f':SENS:FREQ:STOP?').lstrip('+'))
		points = int(self.transport.send(":SENS:SWE:POIN?").lstrip('+'))
		step = (freq_stop - freq_start) // (points - 1)
		self.freq_trace = list(map(str, base.frange(freq_start, freq_stop, step)))

		self.transport.send_err_opc(':TRIGger:SEQuence:SOURce MANual')
		self.transport.send_err_opc(':TRIGger:SEQuence:SCOPe CURRent')

		if kwargs.get("matrix"):
			for ch in self.channels:
				self.transport.send_err_opc(f':SENSe{ch}:SWEep:MODE SINGle')
		else:
			self.transport.send_err_opc("TRIG:SCOP ALL")

		self.transport.send_err_opc(f":INITiate:IMMediate", timeout=10000)

	def config_transmit(self, **kwargs):
		power = kwargs.get("power", 0)
		source_port = kwargs.get("source_port", 1)
		external = kwargs.get("external")

		self.transport.send_err_opc(':SOURce:POWer:COUPle 0')
		self.transport.send_err_opc(':SOURce:POWer1:MODE OFF')
		self.transport.send_err_opc(':SOURce:POWer2:MODE OFF')
		self.transport.send_err_opc(':SOURce:POWer3:MODE OFF')
		self.transport.send_err_opc(':SOURce:POWer4:MODE OFF')
		self.transport.send_err_opc(':SOURce:POWer5:MODE OFF')

		if external:
			external = 'Device0'
			self.transport.send_err_opc(f':SYSTem:CONFigure:EDEVice:DTYPe "{external}","Source"')
			self.transport.send_err_opc(f':SYSTem:CONFigure:EDEVice:DRIVer "{external}","PSG_Vector"')
			self.transport.send_err_opc(f':SYSTem:CONFigure:EDEVice:STATe "{external}",1')
			self.transport.send_err_opc(f':SOURce:POWer6:MODE ON')
			self.transport.send_err_opc(f':SOURce:POWer:LEVel:IMMediate:AMPLitude {power},"{external}"')
		else:
			self.transport.send_err_opc(f':SOURce:POWer{source_port}:MODE ON')
			self.transport.send_err_opc(f':SOURce:POWer1:LEVel:IMMediate:AMPLitude {power},"Port {source_port}"')

	def config_receive(self, **kwargs):
		bw = kwargs.get("bw", 1000)
		traces = kwargs.get("traces", 1)
		display = kwargs.get("display", False)
		source_port = kwargs.get("source_port", 1)
		reflection = kwargs.get("reflection")

		traces_manual = kwargs.get("traces_manual")

		named_ports = ['A', 'B', 'C', 'D']
		num_ports = [1, 2, 3, 4]
		source_port_name = named_ports[source_port - 1]
		named_ports.remove(source_port_name)
		num_ports.remove(source_port)
		trace_arg = 0 if kwargs.get("external") else source_port

		if traces_manual:
			pass
		else:
			for tr in range(traces):
				tr_name = f'{named_ports[tr]}/{source_port_name}'
				tr_param = f"{tr_name},{trace_arg}" if not reflection else f"S{num_ports[tr]}{num_ports[tr]}"
				self.transport.send_err_opc(
					f':CALCulate1:CUSTom:DEFine "TR{tr+1}","Standard","{tr_param}"')
				if display:
					self.transport.send_err_opc(f':DISPlay:WINDow:TRACe{tr+1}:FEED "TR{tr+1}"')

		self.transport.send_err_opc(f':SENSe:SWEep:MODE HOLD')
		self.transport.send_err_opc(F':SENSe:BANDwidth:RESolution {bw}')

		if freq_range := kwargs.get("freq"):
			freq_start, freq_stop, points = freq_range
			self.transport.send_err_opc(f':SENSe:SWEep:POINts {points}')
			self.transport.send_err_opc(f':SENSe:FREQuency:STARt {freq_start}')
			self.transport.send_err_opc(f':SENSe:FREQuency:STOP {freq_stop}')

	def config_receive_range(self, start, stop, points):
		for ch in self.channels:
			self.transport.send_err_opc(f':SENSe{ch}:SWEep:POINts {points}')
			self.transport.send_err_opc(f':SENSe{ch}:FREQuency:STARt {start}')
			self.transport.send_err_opc(f':SENSe{ch}:FREQuency:STOP {stop}')

	def trigger(self, channel=None):
		# self.transport.send(f":SENSe:SWEep:MODE SINGle")
		if channel:
			self.transport.send_err_opc(f":SENSe{channel}:SWEep:MODE SINGle")
		else:
			for channel in self.channels:
				self.transport.send_err_opc(f":SENSe{channel}:SWEep:MODE SINGle")
		self.transport.send_err_opc(f":INITiate:IMMediate", timeout=10000)

	def get_data(self, channel=None):
		# traces_data = [self.freq_trace]
		traces_data = []
		for ch, trs in self.channels.items():
			for tr in trs:
				query_cmd = f":CALCulate:MEASure{tr}:DATA:SDATa?"
				logger.debug(query_cmd)
				data = self.transport.instr.query_ascii_values(query_cmd)
				logger.debug(f"LOAD_DATA: len_data={len(data)} data={data[:3]}...")
				data = list(map(str, data))
				traces_data.append(data[0::2])
				traces_data.append(data[1::2])
		return map(','.join, zip(*traces_data))
		# return zip(self.freq_trace, map(','.join, zip(*traces_data)))  # "freq", "r1","i1","r2","i2", ...
