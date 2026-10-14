from numbers import Number
from typing import Callable

Function = Callable[[Number], Number]

def incremental(x: Number, g: Function) -> Number:
	'''if n == 0:
		return NaN
	if x == 0:
		return 0
	if x < 0 and not (n % 2):
		imag = True'''
	# x = g(y)
	# g(y) - x = 0
	i = (x / 2) or 1
	for _ in range(21):
		if i == 0: break
		if g(i) > x + g(i/2):
			i /= 2
		elif g(i) < x - g(i/2):
			i *= 2
		else:
			break
	gx = 0.5*i
	i = gx / 2
	for _ in range(10):
		for _ in range(32):
			if g(gx + i) < x:
				gx += i
			else: 
				i /= 2
		i /= 10
	if abs(x - g(gx)) >= 1e-15:
		return gx + 1e-15
	return gx

def a(x0: Number, g: Function, lb: Number = 10e-99, ub: Number = 10e99) -> Number:
	# h(y) = g(y) - x = 0
	h = lambda y: g(y) - x0
	x = 0
	i = 1
	if h(0) == 0: return 0
	if abs(h(-1)) < abs(h(1)):
		i = -i
	print(x, i, h(x+i))
	for _ in range(30):
		if h(x+i): pass
	# z1 + dz * g(z1) / dg
	print(x, i, h(x+i))
	