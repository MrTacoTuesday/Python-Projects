from rarity import Rarity, HasRarity
from utils import Named, Attributed, Identified, concat


class ItemType(Named, Identified):

	def __init__(self, name: str):
		super().__init__(name)
		setattr(ItemType, name.replace(" ", ""), self)

	def description(self):
		return self.getname()


ItemType("Tool")

ItemType("Equipment")

ItemType("Artifact")
ItemType("Food")
ItemType("Potion")
ItemType("Resource")


class Item(HasRarity, Identified, Attributed):
	ALL = {}

	def __init__(self,
	             name: str,
	             type: ItemType = ItemType.Resource,
	             rarity: Rarity = Rarity.Common):
		self.type = type
		Item.ALL[id] = self
		super().__init__(name, rarity)

	def extralore(self):
		return concat(self.rarity.getlore(),
		              self.rarity.describe(self.type.getname()),
		              "'" + self.getlore() + "'")
