from uuid import UUID, uuid4

from ATTRIBUTE.attribute_map import AttributeMap
from ENTITY.RACE.race_instance import RaceInstance

from .entity import Entity


class Player(Entity):

    def __init__(self,
                 id: UUID,
                 attributes: AttributeMap,
                 race: RaceInstance,
                 level: int = 0,
                 age: int = 0,
                 health_ratio: float = 1,
                 mana_ratio: float = 1,
                 stamina_ratio: float = 1,
                 skill_points: int = 7):
        super().__init__(id,
                         attributes,
                         race,
                         level,
                         age,
                         health_ratio,
                         mana_ratio,
                         stamina_ratio,
                         skill_points,
                         is_ai_controlled=False)
