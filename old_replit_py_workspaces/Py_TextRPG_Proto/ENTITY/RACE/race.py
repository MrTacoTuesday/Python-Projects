from uuid import UUID

from ATTRIBUTE.attribute_map import AttributeMap
from ATTRIBUTE.attributes import Attributes
from ATTRIBUTE.modifier_map import ModifierMap
from RESOURCES.locale import Locale

from .gender import Gender


class Race:

    GENDERS_BINARY: set[Gender] = {Gender.Male, Gender.Female}
    GENDERS_ALL: set[Gender] = {Gender.Male, Gender.Female, Gender.Androgynous}
    GENDERS_NONE: set[Gender] = {Gender.Androgynous}

    REGISTRY: dict[str, "Race"] = {}

    @staticmethod
    def register(race: "Race"):
        if race.name in Race.REGISTRY:
            race = Race.REGISTRY[race.name]
        else:
            Race.REGISTRY[race.name] = race

    @staticmethod
    def get(name: str) -> "Race | None":
        if name not in Race.REGISTRY:
            return None
        return Race.REGISTRY[name]

    def __init__(self, name: str, valid_genders: set[Gender] | None = None):
        self.name = name
        self.defaults: ModifierMap = ModifierMap()
        self.valid_genders = valid_genders or Race.GENDERS_ALL
        Race.register(self)

    def get_name(self) -> str:
        return Locale.get_name(self.name + ".name")

    def set_defaults(self, modifiers: ModifierMap | None = None):
        self.defaults = modifiers or ModifierMap()

    def apply_modifiers(self, attributes: AttributeMap):
        attributes.apply_modifiers(self.defaults)

    def remove_modifiers(self, attributes: AttributeMap):
        attributes.remove_modifiers(self.defaults)

    def is_valid_gender(self, gender: Gender) -> bool:
        return gender in self.valid_genders
