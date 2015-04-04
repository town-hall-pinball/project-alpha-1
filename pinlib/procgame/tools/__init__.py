__all__ = [
	'tools',
	]

import json as _json
import pinproc as _pinproc

def machine_type_from_json(config_path):
	config = _json.load(open(config_path, 'r'))
	machine_type = config['PRGame']['machineType']
	return _pinproc.normalize_machine_type(machine_type)
