

class Place:
	def __init__(self, name: str, type: str):
		self.name = name.title()
		self.type = type
		self.actions = [] 
		self.region = [] # sub-locations
		self.setting = None
	def setin(self, place):
		self.setting = place
		place.region.append(self)
		return self
	def addregion(self, place):
		place.setin(self)
		return self
	def addaction(self, action: str):
		self.actions.append(action)
		return self
	def addactions(self, *actions: str):
		for a in actions: self.addaction(a)
		return self
	def short(self)->str:
		return (self.name + ", a " + self.type)
	def mid(self)->str:
		return ("the " + self.type + " of " + self.name)
	def long(self)->str:
		a = self.short()
		if self.setting: a += (" in " + self.setting.mid())
		return a
	def get(self, idx: int): return self.region[idx]
	def do(self, idx: int, *args):
		return Action[self.actions[idx]](self,*args)
	def showregions(self, withidx: bool = False)->str:
		s = ""
		for i in range(len(self.region)):
			if withidx: s += str(i) + ":\t\t"
			s += self.get(i).short()
			if i+1 < len(self.region):
				s += "\n"
		return s
	def showactions(self, withidx: bool = False)->str:
		s = ""
		for i in range(len(self.actions)):
			if withidx: s += str(i) + ":\t\t"
			s += self.actions[i].title()
			if i+1 < len(self.actions):
				s += "\n"
		return s
	def __repr__(self)->str: return self.long()

def Input(*args: str, idxs: False)->int or str:
	a = input(">>> ")
	print()
	if idxs:
		try: return int(a)
		except: pass
	if a.lower() in args: return a
	return None

def travel(place: Place)->Place:
	print("Where would you like to go?")
	print(place.showregions(True))
	if place.setting: 
		print("E:\t\tSomewhere else in", place.setting.name)
	print("Enter:\tStay here in", place.name)
	print()
	check = None
	while check is None:
		check = Input("e","",idxs=True)
		if isinstance(check, int):
			if check < len(place.region):
				place = place.get(check)
				print("Going to", place.name)
			else: 
				print("You cannot go there")
				check = None
		elif check == "":
			print("Staying in", place.name)
		elif check.lower() == "e" and place.setting:
			print("Checking the",place.setting.name,"map...")
			return travel(place.setting)
		print()
	return place

def regiontravel(place: Place)->Place:
	print("Where would you like to go?")
	print(place.showregions(True))
	print()
	check = None
	while check is None:
		check = Input(idxs=True)
		if check < len(place.region):
			place = place.get(check)
			print("Going to", place.name)
		else: 
			print("You cannot go there")
			check = None
		print()
	return place

Action = {
	"travel": travel,
	"regiontravel": regiontravel
}

World = {
	"get": Place("Monkey","world"),
	"current": None
}

def setworld(place: Place): World["get"] = place
def world()->Place: return World["get"]
def current()->Place: return World["current"]

def welcome():
	print("Welcome, brave hero, to", world().mid() + ".")
	print()

segments = [
	"Once, long ago, there was a "
]