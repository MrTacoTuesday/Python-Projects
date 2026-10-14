from typing import TypeVar, AnyStr as String
from .attribute import Attribute


class RangedAttribute(Attribute):
	Self = TypeVar("RangedAttribute.Self", bound="RangedAttribute")

	def __init__(self: Self, id: String, defaultValue: float, minValue: float,
	             maxValue: float):
		super().__init__(id, defaultValue)
		self.minValue = minValue
		self.maxValue = maxValue
		if minValue > maxValue:
			raise ValueError("Minimum value cannot be bigger than maximum value!")
		elif defaultValue < minValue:
			raise ValueError("Default value cannot be lower than minimum value!")
		elif defaultValue > maxValue:
			raise ValueError("Default value cannot be bigger than maximum value!")

	def getMinValue(self: Self) -> float:
		return self.minValue

	def getMaxValue(self: Self) -> float:
		return self.maxValue

	def sanitizeValue(self: Self, value: float) -> float:
		if value.isNaN:
			return self.minValue
		return min(max(value, self.minValue), self.maxValue)

	def __repr__(self: Self) -> String:
		return f"RangedAttribute{'{'}id='{self.descriptionId}', default={self.defaultValue}, bounds=[{self.minValue}, {self.maxValue}]{'}'}"

	toString = __repr__
