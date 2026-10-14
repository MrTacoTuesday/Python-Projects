import research_tests_simulations.old_replit_py_workspaces.PolyPython.parser as parser
from numbers import Number
from collections.abc import Sequence


class Polynomial:

	def __init__(self, l: Sequence or Number, *c: Number, v: chr = "x"):
		self.coeffs = ()
		if isinstance(l, str): self.coeffs = parser.parse_poly(l, v)
		elif isinstance(l, Sequence): self.coeffs = tuple(l)
		else:
			self.coeffs = tuple([l] + [*c])
		self.var = v
		self._unpadding()

	def _count(self, obj) -> int:
		return self.coeffs.count(obj)

	def _len(self) -> int:
		return len(self.coeffs)

	def isZero(self) -> bool:
		if self.coeffs == (): return True
		return self._count(0) == self._len()

	def __repr__(self) -> str:
		val = ""
		for i in range(len(self.coeffs)):
			c = self.coeffs[i]
			p = len(self.coeffs) - i - 1
			s = "+"
			if not isinstance(c, complex):
				s = "+" if c >= 0 else "-"
				if i == 0 and s == "+": s = ""
				elif i != 0: s = " " + s + " "
			else: s = "" if i == 0 else " + "
			if c != 0:
				val += s
				if abs(c) != 1 or p == 0:
					val += str(
					 abs(parser.simplify_num(c)) if not isinstance(c, complex) else c)
				if p != 0:
					val += self.var
					if p != 1: val += "^" + str(p)
		if val == "": val += "0"
		return val

	def _padding(self, to: int):
		if len(self.coeffs) >= to: return self
		a = list(self.coeffs)
		while len(a) < to:
			a = [0] + a
		self.coeffs = tuple(a)
		del a, to
		return self

	def _unpadding(self):
		if len(self.coeffs) == 0: return self
		a = list(self.coeffs)
		while len(a) > 0 and a[0] == 0:
			a.pop(0)
		self.coeffs = tuple(a)
		del a
		return self

	def __add__(self, other):
		p1 = list(self._padding(other._len()).coeffs)
		p2 = list(other._padding(self._len()).coeffs)
		self._unpadding()
		other._unpadding()
		del self, other
		ans = []
		for i in range(len(p1)):
			ans.append(p1[i] + p2[i])
		del p1, p2
		return Polynomial(ans)._unpadding()

	def __sub__(self, other):
		return self.__add__(Polynomial(tuple(map(lambda i: -i, other.coeffs))))

	def __mul__(self, other):
		p1 = list(self._padding(len(other.coeffs)).coeffs)
		p2 = list(other._padding(len(self.coeffs)).coeffs)
		self._unpadding()
		other._unpadding()
		if len(p1) == 0 or len(p2) == 0: return None
		if p1.count(0) == len(p1) or p2.count(0) == len(p2): return (0)
		ans = []

		def a(n):
			r, i = 0, 0
			while (n - i >= 0) and (i <= len(p1)):
				r += m(i, n - i)
				i += 1
			del i, n
			return r

		def m(r, c):
			if r >= len(p1) or c >= len(p2): return 0
			return p1[r] * p2[c]

		for idx in range(len(p1) + len(p2) - 1):
			ans.append(a(idx))
		del p1, p2
		return Polynomial(tuple(ans))

	def __truediv__(self, other):
		if self.isZero(): return Polynomial(0)
		if other.isZero(): return None
		if self._len() < other._len(): return (Polynomial(0), self)
		(lead, *trail) = tuple(other.coeffs)
		d = list(map(lambda i: i / lead, self.coeffs))
		v = [lead] + list(map(lambda i: -i / lead, trail))
		del trail
		if len(v) == 1: return Polynomial(tuple(d))
		if len(v) > len(d): return (Polynomial(0), self)
		quos = len(d) - len(v) + 1
		ans = []

		def a(n):
			if n < len(ans): return ans[n]
			ret, i = d[n], 1
			while (n - i >= 0) and (i < len(v)):
				ret += m(i, n - i)
				i += 1
			if n >= len(ans): ans.append(ret)
			del i
			return ret

		def m(r, c):
			return a(c) * v[r] * (0 if (r > 0 and c >= quos) else 1)

		a(len(d) - 1)
		del d, v
		quo = Polynomial(tuple(ans[:quos]))
		rem = Polynomial(tuple(map(lambda i: i * lead, ans[quos:])))
		if rem._count(0) == rem._len(): return quo
		del lead, quos, ans
		return (quo, rem)

	def __floordiv__(self, other):
		res = self / other
		del self, other
		if res == None: return None
		if isinstance(res, Polynomial): return res
		(quo, _) = res
		del res
		return quo

	def __mod__(self, other):
		res = self / other
		del self, other
		if res == None: return None
		if isinstance(res, Polynomial): return Polynomial((0))
		(_, rem) = res
		del res
		return rem


def polydiv(p1: Polynomial or tuple, p2: Polynomial or tuple) -> Polynomial:
	p1 = p1 if isinstance(p1, Polynomial) else Polynomial(p1)
	p2 = p2 if isinstance(p2, Polynomial) else Polynomial(p2)
	return p1 / p2
