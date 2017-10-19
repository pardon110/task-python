import asyncio
import orm


from models import User, Blog, Comment

if __name__ == '__main__':
	loop = asyncio.get_event_loop()

	u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
	u.save()
	
	tasks = [
		asyncio.ensure_future(orm.create_pool(loop)),
		asyncio.ensure_future(u.save())
	]

	loop.run_until_complete(asyncio.wait(tasks))
	loop.close()


