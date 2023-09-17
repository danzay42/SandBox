from typing import Union, Tuple
import pyvisa as visa
import os
import json
import csv

folder_path = str(os.path.dirname(__file__)) + "/"

default_vna = 'default_vna_address'
default_sa = 'default_sa_address'
default_ps = 'default_ps_address'
default_smu_1 = 'default_smu_1_address'
default_smu_2 = 'default_smu_2_address'
default_fg = 'default_fg_address'

technics = 'Measure_technics'
config = 'Config'
num = 'num'
title = 'title'
label = 'label'
description = 'description'
pic = 'pic'
steps = 'steps'
action = 'action'
file = 'file'
cmd_range = 'cmd_range'
action_args = "action_args"
acquire_timeout = 'acquire_timeout'

line_cmd_connect = 'Connect'
line_cmd_wait = 'Wait'
line_cmd_comment = 'Comment'

# cmds_path = 'scpi_cmds_path'
# acquire = 'ACQuire'
# cmd_from = 'scpi_cmd_from'
# cmd_to = 'scpi_cmd_to'
# arg = 'parameter'

	
class SCPI:
	Step: int
	Instrument: str
	Code: str
	Results: str
	
	a_type: str
	a_configuration: str
	a_address: str
	a_commandSet: str
	a_comment: str
	a_ms_timeout: int
	
	def __init__(self, step, instr, code, res=''):
		self.Step = step
		self.Instrument = instr
		self.Code = code.strip()
		self.Results = res
		if code.startswith('(') or code.startswith('#'):
			self.exec = self.exec_action
			self.parse_action_line(code)
		else:
			self.exec = self.exec_usual
	
	def __str__(self):
		return self.Code
	
	def __repr__(self):
		return f"{self.Step}_{self.Instrument}_{self.Code}"

	def exec_usual(self):
		return self.Code
	
	def exec_action(self):
		if self.a_type == line_cmd_connect:
			return self.connect()
		elif self.a_type == line_cmd_wait:
			return self.ms_timeout()
		elif self.a_type == line_cmd_comment:
			return self.comment()
	
	def connect(self):
		return self.a_address
	
	def ms_timeout(self):
		return self.a_ms_timeout
	
	def comment(self):
		return self.a_comment
	
	def parse_action_line(self, code: str):
		self.a_type = code.lstrip('(').split(' ')[0] if code.startswith('(') else line_cmd_comment
		if self.a_type == line_cmd_connect:
			self.a_configuration, self.a_address, self.a_commandSet = code.lstrip('(Connect ').rstrip(')').split(',')
		elif self.a_type == line_cmd_wait:
			self.a_ms_timeout = int(code.strip().lstrip('(Wait').rstrip('ms)'))
		elif self.a_type == line_cmd_comment:
			self.a_comment = code.lstrip('#')


def get_json_dict(key=None):
	data = json.load(open(folder_path + "instruction.json", "r", encoding='utf-8'))
	if key:
		data = data[key]
	return data


def parse_csv_file(file_path):
	with open(file_path, "r", encoding='utf-8') as fd:
		lines = list(map(lambda args: SCPI(*args), csv.reader(fd)))[1:]
	return lines


def parse_txt_file(file_path):
	with open(file_path, "r", encoding='utf-8') as fd:
		lines = fd.readlines()
		dev = SCPI(str(0), '', lines[0], '').a_configuration
		lines = [SCPI(str(i), dev, line) for i, line in enumerate(lines)]
	return lines


def parse_iseq_file(file_path):
	return None


def parse_scpi_file(name: str) -> Union[None, list[SCPI]]:
	if name:
		path = folder_path + name
		if name.endswith('.csv'):
			return parse_csv_file(path)
		elif name.endswith('.txt'):
			return parse_txt_file(path)
	else:
		return None
