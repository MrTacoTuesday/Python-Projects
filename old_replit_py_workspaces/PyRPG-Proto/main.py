"""
Must include:


input from a User, Device, Data Stream, or File.

At least one collection (ex. list or tuple).

At least one procedure with at least one parameter.

An algorithm that includes sequencing, selection, and iteration that is in the body of the selected procedure.

A call to the procedure.

Instructions for output (tactile, audible, visual, or textual) based on input and program functionality
"""

from rarity import Rarity, say_rarities
from item import Item, ItemType

say_rarities()
print()

archmage_cloak = Item("Cloak of Randus", ItemType.Equipment, Rarity.getrand(10))
apple = Item("Apple", ItemType.Food, Rarity.Common)
map = Item("Map of Grimhelm", ItemType.Tool,
                    Rarity.Rare)
gold_ore = Item("Gold Ore", ItemType.Resource, Rarity.Uncommon)

print(archmage_cloak.extralore(),
      apple.extralore(),
      map.extralore(),
      gold_ore.extralore(),
      sep="\n")
print()
print("You found", archmage_cloak.extralore(), "(x2)")
print("> Keep\n  Discard\n")
print(archmage_cloak, "added to inventory.")
