import re
from typing import Tuple, Optional
from numbers import Number


def parse_poly(string: str, var: chr = "x") -> Tuple[Number]:
	s = string.replace(" ", "").replace(var, "x")
	terms = []
	while len(s) > 0:
		sign, coeff, degree = 1, 1, 0
		if s[0] in "+-":
			sign = int(s[0] + "1")
			s = s[1:]
		if re.search("^\(.+?\)", s) is not None:
			m = re.search("\(.+?\)", s)
			coeff = num_str(m.group())
			s = s[m.end():]
		elif re.search("^\d+\.\d+", s) is not None:
			m = re.search("\d+\.\d+", s)
			coeff = float(m.group())
			s = s[m.end():]
		elif re.search("^\d+", s) is not None:
			m = re.search("\d+", s)
			coeff = int(m.group())
			s = s[m.end():]
		if len(s) > 0:
			if s[0] == ")": s = s[1:]
		if re.match("x\^\d+", s) is not None:
			m = re.search("\d+", s)
			degree = int(m.group())
			s = s[m.end():]
		elif re.match("x", s) is not None:
			degree = 1
			s = s[1:]
		terms.append((sign * coeff, degree))
	highest = sorted(map(lambda i: i[1], terms), reverse=True)[0]
	polylist = [0] * (highest + 1)
	for t in terms:
		polylist[highest - t[1]] = simplify_num(t[0])
	return tuple([*polylist])


def num_str(s: str) -> Optional[Number]:
	if s == "": return 0
	s = eval(s)
	if type(s) is not str: return simplify_num(s)
	try:
		return int(s)
	except:
		try:
			return float(s)
		except:
			try:
				return complex(s)
			except:
				return None


def simplify_num(n: int or float or complex) -> Number:
	if isinstance(n, complex):
		if n.imag != 0: return n
		return simplify_num(n.real)
	i = int(n)
	if n == i: return i
	return n


from wmath import Polynomial


def poly_input(prompt: str, normal: bool = False) -> Polynomial:
	if normal: return Polynomial(input(prompt))
	inp = input(prompt).replace(" ", "").split(",")
	return Polynomial(*map(num_str, inp))