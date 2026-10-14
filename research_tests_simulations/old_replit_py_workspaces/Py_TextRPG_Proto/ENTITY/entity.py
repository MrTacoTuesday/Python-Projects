from math import log as ln
from random import random
from uuid import UUID

from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.ATTRIBUTE.attribute import Attribute
from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.ATTRIBUTE.attribute_handler import AttributeHandler
from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.ATTRIBUTE.attribute_map import AttributeMap
from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.ATTRIBUTE.attribute_modifier import AttributeModifier
from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.ATTRIBUTE.attribute_modifier_type import AttributeModifierType
from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.ATTRIBUTE.attributes import Attributes
from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.UTILS.listener import Listener

from .RACE.gender import Gender
from .RACE.race import Race
from .RACE.race_instance import RaceInstance


class Entity:

    ENTITY_BASE_ATTRIBUTE = UUID(hex="cbbc6f1a-5686-420f-b429-d5e2c697ce8a")
    ENTITY_SPENT_POINTS = UUID(hex="a0c0a9c7-c0a1-4ee3-a3b5-ee8c0d3a0a9c")

    def __init__(self,
                 id: UUID,
                 attributes: AttributeMap,
                 race: RaceInstance,
                 level: int = 0,
                 age: int = 1,
                 health_ratio: float = 1,
                 mana_ratio: float = 1,
                 stamina_ratio: float = 1,
                 skill_points: int = 2,
                 is_ai_controlled: bool = True):
        self.id = id
        self.name: str = repr(self.id)
        self.age = age
        self.race = race
        self.level = level

        self.level_listeners: "list[Listener[Entity]]" = []

        self.isAI: bool = is_ai_controlled

        self.experience_ratio = 1

        self.health_ratio = health_ratio
        self.mana_ratio = mana_ratio
        self.stamina_ratio = stamina_ratio

        self.skill_points = skill_points

        self.attributes = attributes

        self._init_attributes()

        self.level_up()

    def _init_attributes(self):
        self.attributes.clear_listeners()

        self.strength.add_listener(lambda _: (self._update_max_hp(
        ), self._update_atk_dmg(), self._update_max_sta(), self._update_def()))
        self.dexterity.add_listener(lambda _: (self._update_max_hp(
        ), self._update_atk_dmg(), self._update_def()))
        self.vitality.add_listener(lambda _: (self._update_max_hp(
        ), self._update_max_sta(), self._update_def()))
        self.intelligence.add_listener(lambda _: (self._update_max_mp()))
        self.wisdom.add_listener(
            lambda _: (self._update_max_mp(), self._update_atk_dmg()))
        self.luck.add_listener(lambda _: (self._update_crit()))

        self.max_health.add_listener(lambda _: (self.check_health()))
        self.max_mana.add_listener(lambda _: (self.check_mana()))
        self.max_stamina.add_listener(lambda _: (self.check_stamina()))

        self._default_modifiers()

        self._update_max_hp()
        self._update_max_mp()
        self._update_max_sta()
        self._update_atk_dmg()
        self._update_def()
        self._update_crit()

    def _default_modifiers(self):
        self.max_health.add_modifier(
            AttributeModifier(Entity.ENTITY_BASE_ATTRIBUTE,
                              AttributeModifierType.ADDITION, 0))
        self.max_mana.add_modifier(
            AttributeModifier(Entity.ENTITY_BASE_ATTRIBUTE,
                              AttributeModifierType.ADDITION, 0))
        self.max_stamina.add_modifier(
            AttributeModifier(Entity.ENTITY_BASE_ATTRIBUTE,
                              AttributeModifierType.ADDITION, 0))
        self.attack_damage.add_modifier(
            AttributeModifier(Entity.ENTITY_BASE_ATTRIBUTE,
                              AttributeModifierType.ADDITION, 0))
        self.defense.add_modifier(
            AttributeModifier(Entity.ENTITY_BASE_ATTRIBUTE,
                              AttributeModifierType.ADDITION, 0))
        self.critical_chance.add_modifier(
            AttributeModifier(Entity.ENTITY_BASE_ATTRIBUTE,
                              AttributeModifierType.ADDITION, 0))

        self.race.apply_modifiers(self.attributes)

    def _update_max_hp(self):
        v = (3 / 5 * self.vitality.value + 1 / 5 * self.dexterity.value +
             1 / 5 * self.strength.value)**(1.041) * 12
        self.max_health.update_modifier(Entity.ENTITY_BASE_ATTRIBUTE,
                                        lambda _: v)

    def _update_max_mp(self):
        v = (4 / 5 * self.intelligence.value +
             1 / 5 * self.wisdom.value)**(1.049) * 20
        self.max_mana.update_modifier(Entity.ENTITY_BASE_ATTRIBUTE,
                                      lambda _: v)

    def _update_max_sta(self):
        v = (2 / 3 * self.vitality.value +
             1 / 3 * self.strength.value)**(1.055) * 40
        self.max_stamina.update_modifier(Entity.ENTITY_BASE_ATTRIBUTE,
                                         lambda _: v)

    def _update_atk_dmg(self):
        v = (5 / 8 * self.strength.value + 1 / 4 * self.dexterity.value +
             1 / 8 * self.wisdom.value)**(1.034) * 3.14
        self.attack_damage.update_modifier(Entity.ENTITY_BASE_ATTRIBUTE,
                                           lambda _: v)

    def _update_def(self):
        v = (7 / 8 * self.strength.value + 1 / 4 * self.vitality.value -
             1 / 8 * self.dexterity.value)**(1.016)
        self.defense.update_modifier(Entity.ENTITY_BASE_ATTRIBUTE, lambda _: v)

    def _update_crit(self):
        v = (self.luck.value)**0.849 / 100
        self.critical_chance.update_modifier(Entity.ENTITY_BASE_ATTRIBUTE,
                                             lambda _: v)

    @property
    def strength(self) -> AttributeHandler:
        return self.attributes.get(Attributes.Core.STRENGTH)

    @property
    def vitality(self) -> AttributeHandler:
        return self.attributes.get(Attributes.Core.VITALITY)

    @property
    def dexterity(self) -> AttributeHandler:
        return self.attributes.get(Attributes.Core.DEXTERITY)

    @property
    def intelligence(self) -> AttributeHandler:
        return self.attributes.get(Attributes.Core.INTELLIGENCE)

    @property
    def wisdom(self) -> AttributeHandler:
        return self.attributes.get(Attributes.Core.WISDOM)

    @property
    def luck(self) -> AttributeHandler:
        return self.attributes.get(Attributes.Core.LUCK)

    @property
    def max_health(self) -> AttributeHandler:
        return self.attributes.get(Attributes.Supplementary.MAX_HEALTH)

    @property
    def max_mana(self) -> AttributeHandler:
        return self.attributes.get(Attributes.Supplementary.MAX_MANA)

    @property
    def max_stamina(self) -> AttributeHandler:
        return self.attributes.get(Attributes.Supplementary.MAX_STAMINA)

    @property
    def critical_chance(self) -> AttributeHandler:
        return self.attributes.get(Attributes.Supplementary.CRIT_CHANCE)

    @property
    def critical_multiplier(self) -> AttributeHandler:
        return self.attributes.get(Attributes.Supplementary.CRIT_MULT)

    @property
    def attack_damage(self) -> AttributeHandler:
        return self.attributes.get(Attributes.Supplementary.MAX_ATTACK)

    @property
    def defense(self) -> AttributeHandler:
        return self.attributes.get(Attributes.Supplementary.MAX_DEFENSE)

    @property
    def health(self) -> float:
        return self.max_health.value * self.health_ratio

    @property
    def mana(self) -> float:
        return self.max_mana.value * self.mana_ratio

    @property
    def stamina(self) -> float:
        return self.max_stamina.value * self.stamina_ratio

    def try_attack(self, entity: "Entity") -> tuple[float, bool]:
        dmg = self.attack_damage.value * (1 + random()) / 2
        dmg -= entity.defense.value
        if dmg < 0:
            return (0, False)
        if random() <= self.critical_chance.value:
            dmg *= self.critical_multiplier.value
            return (dmg, True)
        return (dmg, False)

    def perform_attack(self, entity: "Entity"):
        dmg, _ = self.try_attack(entity)
        entity.harm(dmg, self)

    @property
    def experience_to_level(self) -> int:
        return 3 + int(self.level**1.9416110387254666)

    @property
    def experience(self) -> int:
        return int(self.experience_ratio * self.experience_to_level)

    @property
    def experience_dropped(self) -> int:
        return max(int(self.experience_to_level * (1.2 + random()) / 2.2), 1)

    def add_level_listener(self, listener: "Listener[Entity]"):
        self.level_listeners.append(listener)

    def level_up(self) -> bool:
        if self.experience_ratio < 1:
            return False
        _exn = self.experience_to_level
        self.level += 1
        self.experience_ratio = (self.experience_ratio -
                                 1) * _exn / self.experience_to_level
        self.skill_points += 3
        if self.isAI:
            self.ai_invest()
        self.heal(self.max_health.value)
        self.recover_mana(self.max_mana.value)
        self.recover_stamina(self.max_stamina.value)
        for listener in self.level_listeners:
            listener(self)
        self.gain_experience(0)
        return True

    def invest_sp(self, attribute: Attribute, amount: int = 1) -> int | None:
        amt = min(self.skill_points, amount)
        if amt == 0 or not self.attributes.has(attribute):
            return 0
        handler = self.attributes.get(attribute)
        if not handler.attribute.investable:
            return None
        self.skill_points -= amt
        if not handler.get_modifier(Entity.ENTITY_SPENT_POINTS):
            handler.add_modifier(
                AttributeModifier(Entity.ENTITY_SPENT_POINTS,
                                  AttributeModifierType.ADDITION, 0))
        handler.update_modifier(Entity.ENTITY_SPENT_POINTS, lambda sp:
                                (sp + amt))
        return amt

    def ai_invest(self):
        while self.skill_points > 0:
            investments = {(handler.attribute,
                            handler.get_modifier(Entity.ENTITY_SPENT_POINTS))
                           for handler in self.attributes._map.values()
                           if handler.attribute.investable}
            investments = sorted(investments,
                                 key=lambda x: x[1].amount if x[1] else 0)
            self.invest_sp(investments[0][0], 1)

    def gain_experience(self, amount: int):
        self.experience_ratio += amount / self.experience_to_level
        if self.experience_ratio >= 1:
            self.level_up()

    def heal(self, amount: float | int, source: "Entity | None" = None):
        self.health_ratio += float(amount) / self.max_health.value
        self.check_health(damage_source=source)

    def harm(self, amount: float | int, source: "Entity | None" = None):
        self.health_ratio -= float(amount) / self.max_health.value
        self.check_health(damage_source=source)

    def check_health(self, damage_source: "Entity | None" = None):
        self.health_ratio = max(min(self.health_ratio, 1), 0)
        if self.health_ratio == 0:
            self.die(damage_source)

    def recover_mana(self, amount: float | int):
        self.mana_ratio += float(amount) / self.max_mana.value
        self.check_mana()

    def use_mana(self, amount: float | int):
        self.mana_ratio -= float(amount) / self.max_mana.value
        self.check_mana()

    def check_mana(self):
        self.mana_ratio = max(min(self.mana_ratio, 1), 0)
        if self.mana_ratio == 0:
            #self.has_mana_sickness = True
            # Mana Sickness drains stamina to recover 5% mana
            pass

    def recover_stamina(self, amount: float | int):
        self.stamina_ratio += float(amount) / self.max_stamina.value
        self.check_stamina()

    def use_stamina(self, amount: float | int):
        self.stamina_ratio -= float(amount) / self.max_stamina.value
        self.check_stamina()

    def check_stamina(self):
        self.stamina_ratio = max(min(self.stamina_ratio, 1), 0)
        if self.stamina_ratio == 0:
            #self.has_fatigue = True
            # Fatigue drains health to recover 5% stamina
            pass

    def set_name(self, name: str):
        self.name = name

    def set_age(self, value: int):
        self.age = value

    def set_race(self, race: Race):
        self.race.change_race(race, self.attributes)

    def set_gender(self, gender: Gender):
        self.race.change_gender(gender, self.attributes)

    def die(self, source: "Entity | None" = None):
        if source is not None:
            source.gain_experience(self.experience_dropped)

    def printStatusWindow(self, includes_sections: set[int] = {1, 2, 3, 4, 5}):
        print("\33[2;3mStatus Window:\33[0;1;2m")
        if 1 in includes_sections:
            self._status_window_1()
        if 2 in includes_sections:
            self._status_window_2()
        if 3 in includes_sections:
            self._status_window_3()
        if 4 in includes_sections:
            self._status_window_4()
        if 5 in includes_sections:
            self._status_window_5()
        print("\33[0m")

    def _status_window_1(self):
        print("\tName: {}".format(self.name))
        print("\tAge: {}".format(self.age))
        print("\tRace: {} ({})".format(self.race.get_name(),
                                       self.race.get_gender()))
        print("\tClass: {}".format("self.class.name"))
        print()

    def _status_window_2(self):
        print("\tLevel: {:.0f} ({:.1f}%)".format(self.level,
                                                 self.experience_ratio * 100))
        print("\tXP: {:.0f} / {:.0f}".format(self.experience,
                                             self.experience_to_level))
        print("\tSP: {:.0f}".format(self.skill_points))
        print()

    def _status_window_3(self):
        print("\tSTR: {:.1f}".format(self.strength.value))
        print("\tVIT: {:.1f}".format(self.vitality.value))
        print("\tDEX: {:.1f}".format(self.dexterity.value))
        print("\tINT: {:.1f}".format(self.intelligence.value))
        print("\tWIS: {:.1f}".format(self.wisdom.value))
        print("\tLUK: {:.1f}".format(self.luck.value))
        print()

    def _status_window_4(self):
        print("\tHP: {:.0f} / {:.0f} ({:.0f}%)".format(
            self.health, self.max_health.value, self.health_ratio * 100))
        print("\tMP: {:.0f} / {:.0f} ({:.0f}%)".format(self.mana,
                                                       self.max_mana.value,
                                                       self.mana_ratio * 100))
        print("\tSTA: {:.0f} / {:.0f} ({:.0f}%)".format(
            self.stamina, self.max_stamina.value, self.stamina_ratio * 100))
        print()

    def _status_window_5(self):
        print("\tAtk Dmg: {:.1f}".format(self.attack_damage.value))
        print("\tDefense: {:.1f}".format(self.defense.value))
        print("\tCrit: {:.1f}% (x{:.1f})".format(
            self.critical_chance.value * 100, self.critical_multiplier.value))
        print()
