from colorama import Fore, Style
from utils import Named, as_named, concat
from random import randint


class Rarity(Named):
	ALL = []
	PROB = 0

	def __init__(self, name: str, color: Fore, chance: int):
		self.name = name
		self.color = color
		self.chance = chance
		setattr(Rarity, name.replace(" ", ""), self)
		Rarity.ALL.append(self)
		Rarity.PROB += chance

	def describe(self, object: Named or str) -> str:
		return self.color + as_named(object).description() + Style.RESET_ALL

	def getlore(self) -> str:
		return self.describe(self)

	def getrarity(self) -> "Rarity":
		return self

	def getrand(shift: int = 0) -> "Rarity":
		r = randint(1, Rarity.PROB + shift * len(Rarity.ALL))
		for i in Rarity.ALL:
			c = i.chance + shift
			if r <= c: return i
			r -= c
		return Rarity.ALL[-1]

	def __repr__(self) -> str:
		return self.getlore()


Rarity("Common", Style.DIM + Fore.LIGHTBLACK_EX, 563)
Rarity("Uncommon", Style.DIM + Fore.GREEN, 241)
Rarity("Rare", Fore.BLUE, 115)
Rarity("Epic", Fore.LIGHTMAGENTA_EX, 57)
Rarity("Legendary", Style.BRIGHT + Fore.YELLOW, 23)
Rarity("Mythic", Style.BRIGHT + Fore.RED, 1)


class HasRarity(Named):

	def __init__(self, name: str, rarity: Rarity):
		self.rarity = rarity
		super().__init__(name)

	def getrarity(self) -> Rarity:
		return self.rarity or Rarity.Common

	def getlore(self) -> str:
		return self.rarity.describe(self)

	def __repr__(self) -> str:
		return self.getlore()


def say_rarities():
	print("There are", len(Rarity.ALL), "different rarities in the game:")
	a = concat(*Rarity.ALL, sep=", \0") + "."
	a = a.replace("\0", "", len(Rarity.ALL) - 2).replace("\0", "and ")
	print(a)