from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.ATTRIBUTE.attribute_map import AttributeMap
from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.ATTRIBUTE.modifier_map import ModifierMap
from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.RESOURCES.locale import Locale

from .gender import Gender
from .race import Race


class RaceVariant:

    GENDERS_BINARY: set[Gender] = {Gender.Male, Gender.Female}
    GENDERS_ALL: set[Gender] = {Gender.Male, Gender.Female, Gender.Androgynous}
    GENDERS_NONE: set[Gender] = {Gender.Androgynous}

    REGISTRY: dict[str, "RaceVariant"] = {}

    @staticmethod
    def register(race: "RaceVariant"):
        if race.name in Race.REGISTRY:
            race = RaceVariant.REGISTRY[race.name]
        else:
            RaceVariant.REGISTRY[race.name] = race

    @staticmethod
    def get(name: str) -> "RaceVariant | None":
        if name not in Race.REGISTRY:
            return None
        return RaceVariant.REGISTRY[name]

    def __init__(self,
                 name: str,
                 base: Race,
                 valid_genders: set[Gender] | None = None):
        self.name = name
        self.defaults: ModifierMap = ModifierMap()
        self.base_race = base
        self.valid_genders = valid_genders or Race.GENDERS_ALL
        RaceVariant.register(self)

    def get_name(self) -> str:
        return Locale.get_name(self.name + ".name")

    def set_defaults(self, modifiers: ModifierMap | None = None):
        self.defaults = modifiers or ModifierMap()

    def apply_modifiers(self, attributes: AttributeMap):
        attributes.apply_modifiers(self.defaults)
        self.base_race.apply_modifiers(attributes)

    def remove_modifiers(self, attributes: AttributeMap):
        self.base_race.remove_modifiers(attributes)
        attributes.remove_modifiers(self.defaults)

    def is_valid_gender(self, gender: Gender) -> bool:
        return gender in self.valid_genders

    def is_correct_race(self, race: Race) -> bool:
        return race is self.base_race
