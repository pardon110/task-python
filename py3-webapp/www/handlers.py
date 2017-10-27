# python3
# coding:utf-8
'''
传说中的控制器
'''
__author__ = 'Pardon110'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio
from coreweb import get, post
from models import Blog,User,Comment,next_id


@get('/')
async def index(request):
	# users = await User.findAll()
	blogs = await Blog.findAll()
	return {
		'__template__':'blogs.html',
		'blogs':blogs
	}


@get('/test')
async def test(request):
	summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
	b = Blog(id='389797979', name='Learn Swift', summary=summary, created_at=time.time()-7200)
	await b.save()

