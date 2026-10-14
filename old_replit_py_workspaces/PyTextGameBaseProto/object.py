from typing import Any, List, Protocol
from uuid import uuid4
from tests import Cond


class Object:

	def __init__(self):
		self.id = uuid4()
		self.isHidden = False
		self.isLocked = False
		self.description = None
		self.tags = []
		self.conditions = []

	def IS(self, other) -> bool:
		return self.id == other.id

	def COPY(self, other):
		self.id = other.id
		self.isHidden = other.isHidden
		self.isLocked = other.isLocked
		self.description = other.description
		self.tags = other.tags
		self.conditions = other.conditions
		return self

	def inlist(self, idx: int = None) -> str:
		if self.isHidden or self.isLocked:
			return None
		return (str(idx) + ":\t\t" if idx else "") + repr(self)

	def sethidden(self, to: bool = True):
		self.isHidden = to
		return self

	def setlocked(self, to: bool = True):
		self.isLocked = to
		return self

	def addtags(self, *list: str):
		for i in list:
			if not list.count(i):
				self.tags.append(i)
		return self

	def addconditions(self, *list: Cond):
		for i in list:
			self.conditions.append(i)
		return self

	def listed(self,
	           list: List[Any],
	           withidx: bool = False,
	           showhidden: bool = False) -> str:
		s = ""
		for i in range(len(list)):
			l = list[i]
			if not showhidden and (l.isHidden or l.isLocked): continue
			if withidx: s += str(i) + ":\t\t"
			s += repr(l).title()
			if i + 1 < len(list):
				s += "\n"
		return s

	def __repr__(self) -> str:
		return self.description


class RegionContainer(Protocol):

	def __init__(self):
		self.regions = []
		super()()

	def addregions(self, *list: Any):
		for i in list:
			self.regions.append(i)
		return self


class ActionContainer(Protocol):

	def __init__(self):
		self.actions = []
		super()()

	def addactions(self, *list: Any):
		for i in list:
			self.actions.append(i)
		return self


class EntityContainer(Protocol):

	def __init__(self):
		self.entities = []
		super()()

	def addactions(self, *list: Any):
		for i in list:
			self.entities.append(i)
		return self


class QuestContainer(Protocol):

	def __init__(self):
		self.quests = []
		super()()

	def addactions(self, *list: Any):
		for i in list:
			self.quests.append(i)
		return self
