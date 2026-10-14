from numbers import Number


def sign(x: Number) -> Number:
	if x < 0:
		return -1
	elif x > 0:
		return 1
	elif x == 0:
		return 0


def same_sign(x: Number, y: Number, zeros: bool = False) -> bool:
	if x or y == 0 and not zeros:
		return False
	return sign(x) == sign(y)


NaN = float("nan")