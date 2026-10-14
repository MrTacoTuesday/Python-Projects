from uuid import UUID

from ATTRIBUTE.attributes import Attributes
from ATTRIBUTE.modifier_map import ModifierMap

from .race_variant import RaceVariant
from .races import Races


class RaceVariants:

    VARIANT_DEFAULT_MODIFIERS: UUID = UUID(
        "a0c1e1e4-a0c1-e1e4-a0c1-e1d2b8f1710a")

    TribalHuman = RaceVariant("race.human.tribal", Races.Human)
    MysticHuman = RaceVariant("race.human.mystic", Races.Human)
    


RaceVariants.TribalHuman.set_defaults(ModifierMap()
    ._put(
        Attributes.Core.INTELLIGENCE,
        RaceVariants.VARIANT_DEFAULT_MODIFIERS,
        "*",
        0.5
    )._put(
        Attributes.Core.WISDOM,
        RaceVariants.VARIANT_DEFAULT_MODIFIERS,
        "*",
        0.5
    )._put(
        Attributes.Supplementary.CRIT_CHANCE,
        RaceVariants.VARIANT_DEFAULT_MODIFIERS,
        "+*",
        0.3
    )
)