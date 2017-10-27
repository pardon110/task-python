# python3
# coding:utf-8
'''
传说中的控制器
'''
__author__ = 'Pardon110'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio
import orm
from coreweb import get, post
from models import Blog,User,Comment,next_id


@get('/')
async def index(request):
	users = await User.findAll()
	return {
		'__template__':'test.html',
		'users':users
	}


@get('/test')
async def test(request):
	# logging.info('test')
	# return 'kkkkkkkk'
	sur = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
	# blogs = [
	# 	Blog(id='1',name='Test Blog',summmary=summary,created_at=time()-120),
	# 	Blog(id='2',name='Something New',summmary=summary,created_at=time()-3600),
	# 	Blog(id='3',name='Learn Swift',summmary=summary,created_at=time()-7200),
	# ]
	# b = Blog(id='1',name='Test Blog',summmary=summary,created_at=time()-120)
	# await b.save()
	
	b= Blog(id='333', user_id='123456789', user_name='hehe',user_image='www.baidu.com', name='Test Blog',summary='intro somehto',created_at=time.time()-120, content=sur)
	# await b.save()
	# blogs = None
	# print(b)
	# uid = next_id()
	# name = 'pardon110 '
	# user = User(id=uid, name=name.strip(), email='72380123@aa.com', passwd='123', image='https://www.gravatar.com/')
	await b.save()
	# logging.info('kkkkk000000000')
	# return {
	# 	'__template__':'blogs.html',
	# 	'blogs':'kkk'
	# }