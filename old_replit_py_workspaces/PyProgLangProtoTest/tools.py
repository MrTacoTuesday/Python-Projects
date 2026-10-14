####			tools.py			####
##		Basic utility functions		##

## Returns the value if present, otherwise return the default value
def ifpresent(value: object, default: object) -> object:
	return default if value is None else value

default = ifpresent

## Performs f(x) if f is present, otherwise returns x
def doifpresent(fx: callable, on: object) -> object:
	if fx is None: return on
	return fx(on)

## Combines values similar to a print statement; returns the string
def concat(*values: object,
           sep: str = None,
           last: str = None,
           end: str = None,
           map: callable = None) -> str:
	result = ""
	sep = default(sep, ", ")
	last = default(last, sep)
	end = default(end, "")
	for i in range(len(values)):
		result += str(doifpresent(map, values[i]))
		c = len(values) - i
		if c > 2:
			result += sep
		elif c == 2:
			result += last
		else:
			result += end
	return result

