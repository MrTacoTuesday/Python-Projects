from ATTRIBUTE.attribute_map import AttributeMap
from ENTITY.RACE.race import Race
from ENTITY.RACE.race_variant import RaceVariant
from RESOURCES.locale import Locale

from .gender import Gender


class RaceInstance:

    def __init__(self, race: Race | RaceVariant, gender: Gender):
        self.race: Race | RaceVariant = race
        self.__setup_gender(gender)

    def get_name(self) -> str:
        return self.race.get_name()

    def get_gender(self) -> str:
        return self.gender.get_name()

    def apply_modifiers(self, attributes: AttributeMap):
        self.race.apply_modifiers(attributes)
        self.gender.apply_modifiers(attributes)

    def remove_modifiers(self, attributes: AttributeMap):
        self.race.remove_modifiers(attributes)
        self.gender.remove_modifiers(attributes)

    def __setup_gender(self, gender: Gender):
        if not self.race.is_valid_gender(gender):
            self.gender = list(self.race.valid_genders)[0]
        else:
            self.gender = gender

    def change_gender(self, gender: Gender, attributes: AttributeMap) -> bool:
        if not self.race.is_valid_gender(gender):
            return False
        self.gender.remove_modifiers(attributes)
        self.gender = gender
        self.gender.apply_modifiers(attributes)
        return True

    def change_race(self, race: Race | RaceVariant, attributes: AttributeMap):
        self.race.remove_modifiers(attributes)
        self.race = race
        self.race.apply_modifiers(attributes)
