from typing import Any
from research_tests_simulations.old_replit_py_workspaces.PyTextGameBaseProto.object import Object
from research_tests_simulations.old_replit_py_workspaces.PyTextGameBaseProto.object import RegionContainer as RC
from research_tests_simulations.old_replit_py_workspaces.PyTextGameBaseProto.object import ActionContainer as AC
from research_tests_simulations.old_replit_py_workspaces.PyTextGameBaseProto.object import EntityContainer as EC
from research_tests_simulations.old_replit_py_workspaces.PyTextGameBaseProto.object import QuestContainer as QC


class Region(Object, RC, AC, EC, QC):

	def __init__(self, name: str, type: str):
		self.name = name
		self.type = type
		self.setting = None
		super().__init__()

	def short(self) -> str:
		return (self.name + ", a " + self.type)

	def mid(self) -> str:
		return ("the " + self.type + " of " + self.name)

	def long(self) -> str:
		a = self.short()
		if self.setting: a += (" in " + self.setting.mid())
		return a

	def setin(self, region):
		self.setting = region
		region.addregions(self)
		return self

	def perform(self, idx: int, *args: Any):
		#return Action[self.actions[idx]](self,*args)
		pass
