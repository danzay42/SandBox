import string
from . import logger


class ScpiParser:
	_admitted_keys: dict
	_original_tree: dict
	_last_node: dict
	_table = str.maketrans('', '', string.ascii_lowercase)
	
	def __init__(self, scpi_tree: dict):
		self._original_tree = scpi_tree
		self._last_node = scpi_tree
		self._admitted_keys = dict()
		self._create_admitted_keys(scpi_tree['*'])
		self._create_admitted_keys(scpi_tree[':'])
		logger.debug(f"SCPI INIT: admitted_key={self._admitted_keys}")
			
	def _create_admitted_keys(self, dict_: dict):
		if isinstance(dict_, dict):
			for key_ in dict_.keys():
				admitted_keys = (key_, key_.translate(self._table))
				self._admitted_keys.update(dict.fromkeys(admitted_keys, key_))
				self._create_admitted_keys(dict_[key_])
		
	def _get_item(self, cmd: str, node: dict):
		if cmd or isinstance(node, dict):
			logger.debug(f"SCPI parse_item: '{cmd}'\n\tnod_keys={node.keys()}")
			next_pos = cmd.find(':')
			if next_pos + 1:
				return self._get_item(
					cmd[next_pos + 1:],
					node.get(self._admitted_keys[cmd[:next_pos]]))
			else:
				self._last_node = node
				node_name, *args = cmd.split(' ')
				item_ = node.get(self._admitted_keys[node_name])
				logger.debug(f"SCPI parsed: node={node_name} args{args}")
				if args:
					return item_(*self.parse_args(''.join(args)))
				else:
					return item_()
				
	def parse_cmd(self, data: str) -> str:
		logger.debug(f"SCPI parse_cmd: '{data}'")
		for cmd in data.split(';'):
			if cmd[0] in '*:':
				node = self._original_tree[cmd[0]]
				cmd = cmd[1:]
			else:
				node = self._last_node
			yield self._get_item(cmd, node)
	
	def parse_args(self, cmd: str):
		return [arg.strip() for arg in cmd.split(',')]

	