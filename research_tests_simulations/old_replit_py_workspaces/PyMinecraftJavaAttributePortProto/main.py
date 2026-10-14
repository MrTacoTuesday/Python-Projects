"""from game import Game#, Deps, Handler
from player import Food
from modifier import Modifier, Operation

game = Game()

coffee = (Food("coffee")
 	.set("hunger", Modifier(Operation.SUB, 16))
	.set("thirst", Modifier(Operation.ADD, 2))
	.set("stamina", Modifier(Operation.ADD, 30)))
print(coffee)


#game.init()"""

"""def l1(deps): 
	if deps.game.ticks % 10 == 0:
		print("Listener 1,\t\tTick:\t\t", deps.game.ticks)

def l2(deps): 
	if deps.game.ticks % 36 == 0:
		print("Listener 2, Tick", deps.game.ticks)

game.addTickListener(Handler(
	deps=Deps(Game.Tick),
	onCall=l1,
	daemon=True
))
game.addTickListener(Handler(
	deps=Deps(Game.Tick),
	onCall=l2,
	daemon=True
))"""

"""from attributes import *
Attribute"""

class Bytes:
	def __init__(self, *bytes: bool):
		self.__storage__ = tuple(bytes)

	def __repr__(self):
		return repr(self.__storage__)

	def __len__(self)->int:
		return len(self.__storage__)

	def __unpad_end__(self)->tuple:
		strong = []
		weak = []
		flag = False
		for i in reversed(self.__storage__):
			(strong if flag else weak).insert(0, i)
			if i == 1 and not flag:
				strong.insert(0, i)
				flag = True
		return (Bytes(*strong), Bytes(*weak))

	def __unpad_front__(self)->"Bytes":
		strong = []
		flag = False
		for i in self.__storage__:
			if i == 1 and not flag:
				flag = True
			if flag:
				strong.append(i)
		return Bytes(*strong)

	def __unpad__(self)->tuple:
		return self.__unpad_front__().__unpad_end__()

	def __pad__(self, size: int)->"Bytes":
		s2 = size - self.__len__()
		if s2 < 0:
			return self
		return Bytes(*([0]*s2), *self.__storage__)

	def __add__(self, other)->"Bytes":
		a = self.__pad__(other.__len__()).__storage__
		b = other.__pad__(self.__len__()).__storage__
		new = []
		flag = False
		for i in range(len(a)-1, -1, -1):
			d = a[i] + b[i] + flag
			new.insert(0, d % 2)
			if d >= 2:
				flag = True
			else:
				flag = False
		if flag:
			new.insert(0, 1)
		return Bytes(*new)
				
				
