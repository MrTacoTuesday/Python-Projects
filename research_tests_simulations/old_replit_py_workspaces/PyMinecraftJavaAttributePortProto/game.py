from research_tests_simulations.old_replit_py_workspaces.PyMinecraftJavaAttributePortProto.Event import Event, Handler, Manager, Dependencies as Deps, Void
from time import sleep as wait


class Game:
	ticks_per_second = 30

	def __init__(self):
		self.tickUpdates = Manager(Game.Tick, True).setGlobals(self)
		self.tickUpdates.defersTo(self.onTick)
		self.ticks = 0
		self.isActive = False

	def onTick(self):
		self.ticks += 1
		self.tickUpdates.notifyAll()
		if not self.isActive:
			self.tickUpdates.stop()
		wait(1 / Game.ticks_per_second)

	def _active_(self, deps: Deps):
		if self.ticks > 300:
			self.isActive = False

	def addTickListener(self, listener: Handler):
		self.tickUpdates.addListener(listener)

	def init(self):
		self.isActive = True
		self.addTickListener(Void(self._active_, daemon=True))
		self.tickUpdates()


Game.Tick = Event("game_tick_update", ("game", Game))