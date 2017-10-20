# coding:utf-8
# 不带参数的装饰器

def outer(func):
	print('-----outer----print----1')
	def inner():
		print('-----inner---print-----')
		# return '---return---inner----'
		return func()
	return inner


@outer
def test():
	return '---reutrn---test---'

# print test
# print test()


# 自带参数的装饰器
def wrapper(deparam):
	print('----wrapper-------',deparam)
	def outer(func):
		print('---------outer-------',func)
		def inner():
			print('---------inner-----')
			return func()
		return inner
	return outer		

@wrapper('kk')
def test2():
	print('----test2---')
	return '----return----test2'

# print test2()
# 等价于(装饰器的手动调用)
test2 =  wrapper('kk')(test2)
print test2()
