from sys import version_info as v
# python3
# coding:utf-8
# python 协程原理分析 

def fgx():
	n = 1
	while True:
		print('-'*10 + '分割线' + str(n) + '-'*10)
		n +=1
		yield

gg = fgx().next if v.major == 2 else fgx().__next__ 
# nx = gg.next()


def gfn():
	x = 5
	yield x
	x = x +3
	yield x
	x = x *5
	yield x
	z = x + 1
	yield z
	y= yield
	yield y

g = gfn()

# print g.send(None)
# print g.send(1)
# print g.send(2)
# print g.send(3)
# print g.send(3)
# # print g.next()
# # print g.next()
# # print g.send(9)
# # # print g.next()
# # print g.send(2)
# # print g.next()
# 



def old_fib(n):
	res = [0] * n
	index = 0
	a,b = 0,1
	while index < n:
		res[index] = b
		a, b = b, a+b
		index +=1
	return res



# print old_fib(2)
# print('-'*10 + 'test old fib' + '-'*10)
# for fib_res in old_fib(10):
# 	print(fib_res)

gg()
# print gg.__name__
# c = object

def fib(n):
	index = 0
	a = 1
	b = 2
	while index < n:
		#yield b
		sl = yield b 
		print(sl, 'yield 1235')
		print(index,'yield---- fib')
		a, b = b, a+b
		index +=1

# for fib_res in fib(10):
# 	print(fib_res)
# 	
N = 6
# sfib = fib(N)
# fib_res = sfib.next()
# print fib_res

# gg()
# print sfib.send('outside--data----')



################################
# yield 解说 （本质，走走停停）
# ##############################
# 当一个函数中包含有yield语句时， python会将其自动识别为一个生成器函数
# 当调用生成器函数时，该函数体并不会被调用，得到的是以函数体生成的生成器对象实例,又称为生成器
# yield 可以保留生成器函数的计算现场，暂停生成器函数的执行并将yield 后表达式的值返回给生成器(生成器对象实例）的调用者
# python3.3- 生成器的__next__方法（或使用next函数），唤醒生成器函数体的执行，执行到下一个yield语句处，直到抛出StopIteration异常
# python2 使用next方法唤醒，所谓唤醒即继续执行后面的语句，直到碰到下一个yield停下
# 强调 单纯 yield 类似return 将yiedl后值，交给外部控制者

##########################
# send 来了 
# ########################
#  yield 不是return , return 会将其后面的值返回，中断块级内程序运行
#  b = yield expre    b 值 可由send方法向yield表达式的返回值，该返回值是在当前yield表达式中断时触发
#  生成器 send(None)， 第一次必须参数None 

#####################
# yield from 处理了种异常 
#####################
# yield from 作用 用于重构生成器
# 可以像管理一样将send信息传给内层协程,即将参数作为内层协程的返回值
# 同时yield from 已经处理了各种异常情况 

def copy_fib(i):
	print('I am copy from flib')
	yield from fib(i)
	print('Copy end')


c = copy_fib(3)
print(c.__next__())
gg()
print(c.send('second param'))
gg()
print(c.__next__())
gg()
print(c.__next__())


