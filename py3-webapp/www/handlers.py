# python3
# coding:utf-8
'''
传说中的控制器
'''
__author__ = 'Pardon110'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio
from coreweb import get, post
from models import User, Comment, Blog, next_id

@get('/')
async def index(request):
	users = await User.findAll()
	return {
		'__template__':'test.html',
		'users':users
	}
