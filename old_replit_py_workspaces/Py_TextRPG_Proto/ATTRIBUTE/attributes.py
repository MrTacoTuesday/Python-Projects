from .attribute import Attribute

_ATTRIBUTE_REGISTRY: dict[str, Attribute] = {}


def register(attribute: Attribute) -> Attribute:
    if attribute.name in _ATTRIBUTE_REGISTRY:
        return attribute
    _ATTRIBUTE_REGISTRY[attribute.name] = attribute
    return attribute


class Attributes:

    @staticmethod
    def REGISTRY() -> dict[str, Attribute]:
        return _ATTRIBUTE_REGISTRY

    class Core:
        STRENGTH = register(Attribute("STR", 1))
        VITALITY = register(Attribute("VIT", 1))
        DEXTERITY = register(Attribute("DEX", 1))
        INTELLIGENCE = register(Attribute("INT", 1))
        WISDOM = register(Attribute("WIS", 1))
        LUCK = register(Attribute("LUK", 1))

    class Elemental:
        EARTH = register(Attribute("EARTH AFF", 0))
        FIRE = register(Attribute("FIRE AFF", 0))
        WATER = register(Attribute("WATER AFF", 0))
        AIR = register(Attribute("AIR AFF", 0))
        LIGHT = register(Attribute("LIGHT AFF", 0))
        DARK = register(Attribute("DARK AFF", 0))

        EARTH_RES = register(Attribute("EARTH RES", 0))
        FIRE_RES = register(Attribute("FIRE RES", 0))
        WATER_RES = register(Attribute("WATER RES", 0))
        AIR_RES = register(Attribute("AIR RES", 0))
        LIGHT_RES = register(Attribute("LIGHT RES", 0))
        DARK_RES = register(Attribute("DARK RES", 0))

    class Supplementary:
        MAX_HEALTH = register(Attribute("max hp", 0, investable=False))
        MAX_MANA = register(Attribute("max mana", 0, investable=False))
        MAX_STAMINA = register(Attribute("max stamina", 0, investable=False))
        MAX_ATTACK = register(Attribute("attack dmg", 0, investable=False))
        MAX_DEFENSE = register(Attribute("defense", 0, investable=False))
        CRIT_CHANCE = register(Attribute("crit", 0, investable=False))
        CRIT_MULT = register(Attribute("crit mult", 1.5, investable=False))
