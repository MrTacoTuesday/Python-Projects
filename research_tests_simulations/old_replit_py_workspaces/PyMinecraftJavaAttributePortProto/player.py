from typing import TypeVar, AnyStr as String
from property import Property, NProperty
from modifier import Modifier, ModifierMap


class Player:
	Self = TypeVar("Self", bound="Player")

	def __init__(self: Self):
		self.fullness = NProperty("fullness", 1, 0, 100)
		self.stamina = NProperty("stamina", 80, 0, 100)
		self.agility = NProperty("agility", 1, 0, 100)
		self.properties = {}
		self.modifiers = ModifierMap()

	def _property(self: Self, property: Property) -> Property:
		self.properties

	def addModifier(self: Self, name: String, property: Modifier):
		if self.hasModifier(name):
			pass
		self.modifiers[name](property)

	def hasModifier(self: Self, name: String) -> bool:
		return name in self.modifiers

	def getModifier(self: Self, name: String) -> Modifier:
		for p in self.modifiers:
			if p.name == name:
				return p
		return None

	def consume(self: Self, food: "Food"):
		for i in food.properties:
			if self.hasModifier(i):
				food.get(i).apply(self.getModifier(i))

	def __repr__(self: Self) -> String:
		return repr(self.modifiers)


class Food:
	Self = TypeVar("Self", bound="Food")

	def __init__(self: Self, name: String):
		self.name: String = name
		self.properties: ModifierMap = ModifierMap()

	def set(self: Self, name: String, value: Modifier) -> Self:
		self.properties[name] = value
		return self

	def get(self: Self, name: String) -> Modifier:
		return self.properties[name]