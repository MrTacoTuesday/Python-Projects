from enum import Enum
from random import randrange as rnd


class Color(Enum):
	Red = "\33[31m"
	Black = "\33[30m"

	def inverted(self) -> "Color":
		return Color.Red if self is Color.Black else Color.Black

	def wrap(self, txt: str) -> str:
		return f"{self.value}{txt}\33[0m"


class Suite:
	ALL = []

	def __init__(self,
	             name: str,
	             uc: int,
	             iuc: int,
	             color: Color,
	             joker: bool = False, inverse: "Suite" = None):
		self.name = name
		self.char = uc
		self.ichar = iuc
		self.color = color
		self.isJoker = joker
		self.inverse = inverse

	def save(self) -> "Suite":
		if not Suite.ALL.count(self):
			Suite.ALL.append(self)
			setattr(Suite, self.name, self)
		return self

	def get(self) -> str:
		return chr(self.char)

	def colored(self) -> str:
		return self.color.wrap(self.get())

	def inverted(self) -> "Suite":
		if self.inverse: 
			if not self.inverse.inverse:
				self.inverse.inverse = self
			return self.inverse
		return Suite(self.name, self.ichar, self.char, self.color.inverted(),
		             self.isJoker, inverse=self)

	def random(jokers: bool = False) -> "Suite":
		_kys = [*Suite.ALL]
		if jokers: _kys.append(Suite.Joker)
		return _kys[rnd(0, len(_kys))]

	def __repr__(self) -> str:
		return "Suite." + self.name


Suite("Spades", 0x2660, 0x2664, Color.Black).save()
Suite("Hearts", 0x2665, 0x2661, Color.Red).save()
Suite("Diamonds", 0x2666, 0x2662, Color.Red).save()
Suite("Clubs", 0x2663, 0x2667, Color.Black).save()
Suite.Joker = Suite("Joker", 0x265B, 0x265B, Color.Red, True) #0x2655 is a bit thinner


class Value(Enum):
	Ace = "A"
	Two = "2"
	Three = "3"
	Four = "4"
	Five = "5"
	Six = "6"
	Seven = "7"
	Eight = "8"
	Nine = "9"
	Ten = "10"
	Jack = "J"
	Queen = "Q"
	King = "K"
	Special = ""

	def get(self, highace: bool = False) -> int:
		if self.value == "":
			return 0
		if self.value in "JQK":
			return (11 + "JQK".index(self.value))
		if self == Value.Ace:
			return (15 if highace else 1)
		return int(self.value)

	def front(self)->str:
		if self is Value.Special: return ""
		return self.name + " Of "

	def random(jokers: bool = False) -> "Value":
		_kys = [*Value._member_names_, *Value._member_names_]
		_kys.remove("Special")
		if not jokers: _kys.remove("Special")
		return getattr(Value, _kys[rnd(0, len(_kys))])


class Card:

	def __init__(self,
	             value: Value,
	             suite: Suite,
	             highace: bool = False,
	             inverted: bool = False, brand: "Deck" = None):
		self.value = value
		self.suite = suite
		self.highace = highace
		self.inverted = inverted
		self.brand = brand

	def txt(self) -> str:
		if self.inverted:
			return (self.value.value + self.suite.inverted().get())
		return (self.value.value + self.suite.get())

	def colored(self) -> str:
		return self.suite.color.wrap(self.txt())

	def inverted(self) -> "Card":
		return Card(self.value, self.suite.inverted(), self.highace,
		            not self.inverted)

	@property
	def belongsToDeck(self)->bool:
		return self.brand is not None

	def match(self, other: "Card")->bool:
		return (self.value is other.value and
		self.suite is other.suite)

	def samesettings(self, other: "Card")->bool:
		pass

	def __repr__(self) -> str:
		return self.colored()

	def longrepr(self)->str:
		return self.suite.color.wrap(self.value.front()+self.suite.name)

	def random(jokers: bool = None,
	           highace: bool = None,
	           inverted: bool = None) -> "Card":
		_jok = jokers if jokers is not None else bool(rnd(0, 2))
		_val = Value.random(_jok)
		if _val is Value.Special:
			_sui = Suite.Joker
			if rnd(0, 2) == 1:
				_sui = _sui.inverted()
		else:
			_sui = Suite.random()
		_ace = highace if highace is not None else bool(rnd(0, 2))
		_inv = inverted if inverted is not None else bool(rnd(0, 2))
		return Card(_val, _sui, _ace, _inv)


class Deck:

	def __init__(self,
	             jokers: bool = False,
	             highace: bool = False,
	             inverted: bool = False):
		self.jokers = jokers
		self.highace = highace
		self.inverted = inverted
		self.cards = []
		self.renew()

	def renew(self):
		for suite in Suite.ALL:
			for value in Value:
				if value is Value.Special: continue
				self.cards.append(Card(value, suite, self.highace, self.inverted, brand=self))
		if not self.jokers: return
		self.cards.append(
		 Card(Value.Special, Suite.Joker, self.highace, self.inverted, brand=self))
		self.cards.append(
		 Card(Value.Special, Suite.Joker.inverted(), self.highace, self.inverted, brand=self))

	def randomize(self):
		_cds = [*self.cards]
		_res = []
		for _ in range(len(self.cards)):
			_res.append(_cds.pop(rnd(0, len(_cds))))
		self.cards = _res

	def draw(self, randomly: bool = False, replace: bool = True) -> Card:
		_idx = rnd(0, len(self.cards)) if randomly else 0
		_crd = self.cards.pop(_idx)
		if replace:
			_idx = rnd(0, len(self.cards) + 1) if randomly else len(self.cards)
			self.cards.insert(_idx, _crd)
		return _crd

	def multidraw(self, amount: int = 1, randomly: bool = False, replace: bool = True) -> list:
		_res = []
		for _ in range(amount):
			if not len(self.cards) and not replace:
				_war = Warning(f"""Could only draw {len(_res)} cards, since no cards are left in the deck""")
				raise _war
			_res.append(self.draw(randomly, replace))
		return _res

	def holdAll(self, cards: list):
		for i in cards:
			self.cards.append(i)
				

	def __getitem__(self, _idx: int)->Card:
		return self.cards[_idx]

	def __len__(self)->int:
		return len(self.cards)

	def random(jokers: bool = None,
	           highace: bool = None,
	           inverted: bool = None) -> "Deck":
		_jok = jokers if jokers is not None else bool(rnd(0, 2))
		_ace = highace if highace is not None else bool(rnd(0, 2))
		_inv = inverted if inverted is not None else bool(rnd(0, 2))
		_dek = Deck(_jok, _ace, _inv)
		_dek.randomize()
		return _dek

class Hand: #... slf.capacity = 7
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.cards = []
	def hold(self, card: Card):
		self.cards.append(card)
	def holdAll(self, cards: list):
		for i in cards:
			self.cards.append(i)
	def take(self, deck: Deck, amount: int = 1, randomly: bool = False):
		self.holdAll(deck.multidraw(amount, randomly=randomly, replace=False))


deck = Deck()
deck.randomize()
player = Hand(7)
player.take(deck, 2)
print(deck.cards)
print(player.cards)
