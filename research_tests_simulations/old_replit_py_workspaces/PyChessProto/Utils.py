#from collections.abc import Sequence
from typing import Callable, Iterable, ParamSpec, TypeVar

_T1 = ParamSpec("_T1")
_S = TypeVar("_S")

def self(obj: _S)->_S:
	return obj

def iter_str(obj: Iterable[_T1],
			 using: Callable[[_T1], _S] = self,
             sep: str = ", ",
             last: str = ", ") -> str:
	_res = ""
	for i in obj:
		_res += str(using(i))
		if len(obj) > 1 and i is obj[-2]:
			_res += last
		elif i is not obj[-1]:
			_res += sep
	return _res