#from typing import Protocol
from typing import Optional, Any


class Named:

	def __init__(self, name: str):
		self.name = name

	def getname(self) -> str:
		return self.name

	def description(self) -> str:
		return self.name

	def __repr__(self) -> str:
		return self.getname()


class Attributed:

	def __init__(self):
		pass

	def attr(self, name: str, set: Optional[Any] = None) -> Any:
		if not set: return getattr(self, name, None)
		setattr(self, name, set)


def as_named(inp: Named or str) -> Named:
	if isinstance(inp, str): inp = Named(inp)
	return inp


from uuid import UUID, uuid4


class Identified:
	ALL = {}

	def __init__(self, id: UUID = None):
		if id and Identified.ALL.get(id):
			pass  # throw error
		self.id = id or uuid4()
		Identified.ALL[id] = self


def concat(*string, sep: str = " ", end=""):
	result, l = "", list(string)
	ls = len(l)
	for i in range(ls):
		a = l[i]
		if not isinstance(a, str): a = repr(a)
		result += a + (end if i + 1 >= ls else sep)
	return result
