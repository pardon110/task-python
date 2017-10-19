# !/usr/bin/python3
# coding:utf-8

__author__ = 'Pardon110'

'''
JSON API definition
'''

import json, logging, inspect, functools

class APIError(Exception):
	'''
	the base APIError which contains error(required),data(ooptional) and message(opitonal).
	'''
	def __init__(self, error, data='', message=''):
		super(APIError, self).__init__(message)
		self.error = error
		self.data = data
		self.message = message


class APIValueError(APIError):
	'''
    Indicate the input value has error or invalid. The data specifies the error field of input form.
    '''
	def __init__(self, field, message=''):
		super(APIValueError,self).__init__('value:invalid',field, message)


class APIResourceNotFoundError(APIError):

	def __init__(self, field, message=''):
		super(APIResourceNotFoundError, self).__init__('value:notFound',field,message)


class APIPermissionError(APIError):	
	"""docstring for APIPermissionError"""
	def __init__(self, message=''):
		super(APIPermissionError, self).__init__('permission:forbidden', 'permission', message)
