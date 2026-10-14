from math import factorial


def C(n: int, r: int):
	return int(factorial(n) / (factorial(n - r) * factorial(r)))


def pascal(r: int, c: int):
	return C(r, c)


def binomialexpansion(a, b, n: int = 2):
	terms = []
	for i in range(n + 1):
		terms.append(pascal(n, i) * a**(n - i) * b**i)
	del a, b, n
	return tuple(terms)


binexp = binomialexpansion


def summation(k: int, n: int, fx: callable):
	r = 0
	s = 1 if n >= k else -1
	for i in range(k, n + s, s):
		r += fx(i)
	del k, n, fx, s
	return r


sumk = summation


def product(k: int, n: int, fx: callable):
	r = 1
	s = 1 if n >= k else -1
	for i in range(k, n + s, s):
		r *= fx(i)
	del k, n, fx, s
	return r


def sumC(n):
	return 2**n


from collections.abc import Sequence


def binprob(a, b, n: int, r=None):
	e, d = binexp(a, b, n), (a + b)**n
	del a, b, n
	if r is None: return (e, d)
	if isinstance(r, Sequence):
		l = lambda i: e[i] if i in r else 0
		return sumk(0, len(e) - 1, l) / d
	if isinstance(r, int):
		return e[r] / d
	del e, d, r


from research_tests_simulations.old_replit_py_workspaces.PolyPython.wpoly import Polynomial, polydiv

Polynomial = Polynomial
poly = Polynomial
polydiv = polydiv