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
#	users = await User.findAll()
#	return {
#		'__template__':'test.html',
#		'users':users
#	}

	summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
	blogs = [
		Blog(id='1',name='Test Blog',summmary=summary,created_at=time()-120),
		Blog(id='2',name='Something New',summmary=summary,created_at=time()-3600),
		Blog(id='3',name='Learn Swift',summmary=summary,created_at=time()-7200),
	]
	return {
		'__template__':'blogs.html',
		'blogs':blogs
	}
