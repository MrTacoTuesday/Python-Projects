"""from typing import Tuple, List, TypeAlias, Sequence

Type: TypeAlias = type or Tuple[type]
def _tupletype(*_T: Type)->Type:
	_t: List[Type] = []
	for T in _T:
		if isinstance(T, Sequence):
			for t in _tupletype(*T):
				if _t.count(t) == 0: 
					_t.append(t)
		else:
			if _t.count(T) == 0: 
				_t.append(T)
	return tuple(_t)"""



import Type
