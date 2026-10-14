from typing import TypeVar, AnyStr as String


class Attribute:
	Self = TypeVar("Attribute.Self", bound="Attribute")

	MAX_NAME_LENGTH = 64

	def __init__(self: Self, id: String, defaultValue: float):
		self.descriptionId = id
		self.defaultValue = defaultValue
		self.syncable = False

	def setSyncable(self: Self, value: bool = True) -> Self:
		self.syncable = value
		return self

	def getDefaultValue(self: Self) -> float:
		return self.defaultValue

	def isClientSyncable(self: Self) -> bool:
		return self.syncable

	def sanitizeValue(self: Self, value: float) -> float:
		return value

	def getDescriptionId(self: Self) -> String:
		return self.descriptionId

	def __repr__(self: Self) -> String:
		return f"Attribute{'{'}id='{self.descriptionId}', default={self.defaultValue}{'}'}"

	toString = __repr__
