# !python3
# coding:utf-8
# config.py
'''
Configuration
'''


__author__ = 'Pardon110'

import config_default

class Dict(dict):
	'''
	Simple dict but support access x.y style
	'''
	def __init__(self, name = (), values = (), **kw):
		super(Dict, self).__init__(**kw)
		for k, v in zip(name, values):
			self[k] = v

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Dict' object has no attribute '%s' " % key)

	def __setattr__(self, key, value):
		self[key] = value



# 递归覆盖 
def merge(defaults, override):
	r = {}
	for k, v in defaults.items():
		if k in override:
			if isinstance(v, dict):
				r[k] = merge(v, override[k])
			else:
				r[k] = override[k]
		else:
			r[k] = v
	return r


# 字典数据处理
def toDict(d):
	D = Dict()
	for k, v in d.items():
		D[k] = toDict(v) if isinstance(v, dict) else v
	return D


configs = config_default.configs

try:
	import config_override
	configs = merge(configs, config_override.configs)
except ImportError:
	pass


# 转成字典格式
configs = toDict(configs)

