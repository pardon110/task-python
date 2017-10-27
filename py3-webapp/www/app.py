# !python3
# coding:utf-8
'''
async web application
'''


import logging;logging.basicConfig(level=logging.INFO)

import asyncio,os,json,time
from datetime import datetime

from aiohttp import web
from jinja2 import Environment, FileSystemLoader,filters

import orm
from coreweb import add_routes, add_static

#import pudb;pu.db

# 初始化模板引擎
def init_jinja2(app,**kw):
	logging.info('init jinja2...')
	options = dict(
		autoescape = kw.get('autoescape', True),
		block_start_string = kw.get('block_start_string', '{%'),
		block_end_string = kw.get('block_end_string', '%}'),
		variable_start_string = kw.get('variable_start_string', '{{'),
		variable_end_string = kw.get('variable_end_string', '}}'),
		auto_reload = kw.get('auto_reload', True)
	)
	path = kw.get('path',None)
	if path is None:
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/')
	logging.info('set jinja2 template path: %s' % path)
	# 设置模板路径，得到模板对象 
	env = Environment(loader=FileSystemLoader(path), **options)
	filters = kw.get('filters', None)
	if filters is not None:
		for name, f in filters.items():
			env.filters[name]	= f
	app['__templating__'] = env

# 日志记录
async def logger_factory(app, handler):
	async def logger(request):
		logging.info('Request: %s %s' % (request.method, request.path))
		# await asyncio.sleep(0.3)
		return (await handler(request))
	return logger


async def response_factory(app,handler):
	async def response(request):
		logging.info('Response handler...')		
		r =  await handler(request)
		if isinstance(r,web.StreamResponse):
			return r
		if isinstance(r, bytes):
			resp = web.Response(body=r)
			resp.contetnt_type = 'application/octet-stream'
			return resp
		if isinstance(r, str):
			if r.startwith('redirect:'):
				return web.HTTPFound(r[9:])
			resp = web.Response(body=r.encode('utf-8'))
			resp.content_type = 'text/html;charset=utf-8'
			return resp
		if isinstance(r,dict):
			template = r.get('__template__')
			if template is None:
				resp = web.Response(body=json.dump(r, ensure_ascii=False, default=lambda o:o.__dict__).encode('uft-8'))
				resp.content_type = 'application/json;charset=utf-8'
				return resp
			else:
				resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))	
				resp.content_type = 'text/html;charset=utf-8'
				return resp
		if isinstance(r,int) and r >=100 and r < 600:
			return web.Response(r)
		if isinstance(r, tuple) and len(r) == 2:
			t, m = r
			if isinstance(t, int) and t >=100 and t < 600:
				return web.Response(t,str(m))
		#default:
		logging.info('default response...')
		resp = web.Response(body=str(r).encode('utf-8'))
		resp.content_type = 'text/plain;charset=utf-8'
		return resp
	return response

def datetime_filter(t):
	delta = int(time.time() - t)
	if delta < 60:
		return u'1分钟前'
	if delta < 3600:
		return u'%s分钟前' % (delta // 60)
	if delta < 86400:
		return u'%s小时前' % (delta // 3600)
	if delta < 604800:
		return u'%s天前' % (delata // 86400)
	dt = datetime.fromtimestamp(t)
	return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

#filters.FILTERS['datetime'] = datetime_filter

# 初始循环事件句柄 
async def init(loop):
	# 连接数据库
	await orm.create_pool(loop=loop, host='127.0.0.1',port=3306, user='root', password='secret',db='py3web')
	# 创建应用
	app = web.Application(loop=loop,middlewares=[
			logger_factory,response_factory
		])
	# 初始化模板引擎
	init_jinja2(app, filters=dict(datetime=datetime_filter))

	# 批量添加路由模块
	add_routes(app,'handlers')
	add_static(app)

	srv = await loop.create_server(app.make_handler(), '0.0.0.0',8858)
	logging.info('server started at http://0.0.0.0:8858')
	return srv


# 获取异步io操作事件循环句柄
loop = asyncio.get_event_loop()
# 执行协程 
loop.run_until_complete(init(loop))
# 执行事件监听
loop.run_forever()
