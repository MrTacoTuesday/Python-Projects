from uuid import UUID

from ATTRIBUTE.attributes import Attributes
from ATTRIBUTE.modifier_map import ModifierMap

from .race import Race


class Races:

    RACE_DEFAULT_MODIFIERS: UUID = UUID("0e3d6c6a-ee6c-4b0d-a7d6-ee0f5ee0f1ee")
    
    Human: Race = Race("race.human", Race.GENDERS_BINARY)
    Elf: Race = Race("race.elf", Race.GENDERS_ALL)
    Dwarf: Race = Race("race.dwarf", Race.GENDERS_BINARY)
    Orc: Race = Race("race.orc", Race.GENDERS_BINARY)
    Ogre: Race = Race("race.ogre", Race.GENDERS_BINARY)
    
    Celestial: Race = Race("race.celestial", Race.GENDERS_ALL)
    Angel: Race = Race("race.angel", Race.GENDERS_BINARY)
    Demon: Race = Race("race.demon", Race.GENDERS_BINARY)

    Flora: Race = Race("race.flora", Race.GENDERS_ALL)
    Fauna: Race = Race("race.fauna", Race.GENDERS_ALL)


Races.Human.set_defaults(ModifierMap()
    ._put(
        Attributes.Core.INTELLIGENCE,
        Races.RACE_DEFAULT_MODIFIERS,
        "+*",
        0.2
    )._put(
        Attributes.Core.WISDOM,
        Races.RACE_DEFAULT_MODIFIERS,
        "+*",
        0.1
    )._put(
        Attributes.Supplementary.CRIT_CHANCE,
        Races.RACE_DEFAULT_MODIFIERS,
        "+*",
        0.05
    )
)

Races.Elf.set_defaults(ModifierMap()
    ._put(
        Attributes.Core.STRENGTH,
        Races.RACE_DEFAULT_MODIFIERS,
        "*",
        0.5
    )._put(
        Attributes.Core.VITALITY,
        Races.RACE_DEFAULT_MODIFIERS,
        "*",
        0.8
    )._put(
        Attributes.Core.DEXTERITY,
        Races.RACE_DEFAULT_MODIFIERS,
        "+*",
        0.2
    )._put(
        Attributes.Core.INTELLIGENCE,
        Races.RACE_DEFAULT_MODIFIERS,
        "+*",
        0.4
    )._put(
        Attributes.Core.WISDOM,
        Races.RACE_DEFAULT_MODIFIERS,
        "+*",
        0.7
    )._put(
        Attributes.Supplementary.MAX_HEALTH,
        Races.RACE_DEFAULT_MODIFIERS,
        "*",
        1.4
    )._put(
        Attributes.Supplementary.MAX_MANA,
        Races.RACE_DEFAULT_MODIFIERS,
        "*",
        1.1
    )
)