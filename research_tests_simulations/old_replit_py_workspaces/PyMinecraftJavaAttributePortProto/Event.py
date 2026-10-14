class Event:

	def __init__(self, name: str, *args: type):
		self.name = name
		self.kwargs = []
		self.args = []
		for i in range(len(args)):
			k = f"${i}"
			v = args[i]
			if type(v) is tuple:
				if v[0] == "?":
					k += "?"
				else:
					k = v[0]
				v = tuple(v[1:])
			self.kwargs.append(k)
			self.args.append(v)

	def __repr__(self):
		return f"Event<{self.name}>"


class Dependencies(object):

	def __init__(self, event: Event, *args: object):
		self.__event__ = event
		self.__attrs__ = {}
		if len(args):
			self._get_(*args)

	@property
	def _is_empty_(self) -> bool:
		if not len(self.__event__.args):
			return False
		return len(self.__attrs__.keys()) == 0

	def _set_(self, key: str, value: object):
		self.__attrs__[key] = value
		setattr(self, key.replace("?", "").replace("$", "$"), value)

	def _get_(self, *args: object):
		for i in range(len(self.__event__.args)):
			key = self.__event__.kwargs[i]
			type = self.__event__.args[i]
			value = None if len(args) <= i else args[i]
			if self._is_valid_(key, type, value):
				self._set_(key, value)
			else:
				Dependencies._mismatch_(value, key, type)
		return self

	def _is_valid_(self, key: str, type: type, value: object) -> bool:
		optional = "?" in key
		if value is None:
			if not optional:
				return False
		elif not isinstance(value, type):
			return False
		return True

	def _mismatch_(value, name, arg):
		raise TypeError(f"""{
				type(value).__name__
			} value "{value}" does not match argument ({
				name
			}: {
   				str(tuple(map(lambda i: i.__name__, arg)))
	   				.replace("(", "").replace(")", "")
					.replace(", ", " or ").replace("'", "")
	   		})""")

	def new(event: Event, *args: object):
		return Dependencies(event, *args)


from threading import Thread


class Handler:

	def __init__(self, deps: Dependencies, onCall: callable, daemon: bool = None):
		self.thread = Thread(target=self.run, daemon=daemon)
		self.daemon = daemon
		self.event = deps.__event__
		self.dependencies = deps
		self.onCall: callable = onCall
		self._defersTo_: list = []
		self.flagged = False
		self.running = False

	def defersTo(self, *fxs: callable):
		for i in fxs:
			self._defersTo_.append(i)

	def defer(self):
		for method in self._defersTo_:
			method()

	def __call__(self, threaded: bool = True):
		if not self.hasDeps:
			raise Exception(
			 "Handler dependencies have not been set; <use self.setDeps(*args)>")
		if threaded:
			if not self.running:
				self.start()
			self.flag()
		else:
			self.onCall(self.dependencies)

	def setDeps(self, *args: object):
		self.dependencies._get_(*args)
		return self

	@property
	def hasDeps(self) -> bool:
		return not self.dependencies._is_empty_

	def run(self):
		if not self.hasDeps:
			raise Exception(
			 "Handler dependencies have not been set; <use self.setDeps(*args)>")
		#print("Thread sucessfully opened")
		while self.running:
			if self.flagged:
				self.onCall(self.dependencies)
				self.flagged = False
				self.defer()
		#print("Thread finished sucessfully")

	def flag(self):
		self.flagged = True

	def start(self, flag: bool = False):
		self.running = True
		self.thread.start()
		if flag: self.flag()

	def stop(self):
		self.running = False


class Manager:

	def __init__(self, event: Event, hasGlobals: bool = True):
		self.event = event
		self.globals = Dependencies(event)
		self.running = False
		self.listeners = []
		self._defersTo_: list = []

	def addListener(self, handler: Handler):
		if handler.event is not self.event:
			pass
		self.listeners.append(handler)
		handler.defersTo(self._try_defer_)
		self.__setAll__()
		if self.running:
			handler()

	def setGlobals(self, *args: object):
		self.globals._get_(*args)
		self.__setAll__()
		return self

	@property
	def hasControl(self) -> bool:
		return all(map(lambda i: not i.flagged, self.listeners))

	def _try_defer_(self):
		if self.hasControl:
			self.defer()

	def defersTo(self, *fxs: callable):
		for i in fxs:
			self._defersTo_.append(i)

	def defer(self):
		for method in self._defersTo_:
			method()

	def __setAll__(self):
		if self.running and not self.globals._is_empty_:
			for i in self.listeners:
				i.dependencies = self.globals

	def start(self):
		self.running = True
		self.__setAll__()
		for task in self.listeners:
			task()

	def notifyAll(self):
		for task in self.listeners:
			task.flag()

	def stop(self):
		for task in self.listeners:
			task.stop()
		self.running = False

	def __call__(self):
		self.start()


VoidEvent = Event("void")


def Void(onCall: callable = (lambda _: ()), daemon: bool = None) -> Handler:
	return Handler(Dependencies(VoidEvent), onCall, daemon)
