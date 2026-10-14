from typing import Literal
from uuid import UUID, uuid4

from .attribute import Attribute
from .attribute_modifier import AttributeModifier
from .attribute_modifier_type import AttributeModifierType


class ModifierMap:

    def __init__(
        self,
        attr_map:
        "ModifierMap | dict[Attribute, list[AttributeModifier]] | None" = None
    ):
        self._map: dict[Attribute, list[AttributeModifier]] = {}
        if isinstance(attr_map, dict):
            for attr, lst in attr_map.items():
                if not isinstance(attr, Attribute):
                    continue
                if not isinstance(lst, list):
                    continue
                if not all(isinstance(x, AttributeModifier) for x in lst):
                    continue
                self._map[attr] = lst
        elif isinstance(attr_map, ModifierMap):
            self._map = attr_map._map

    def __getitem__(self, attr: Attribute) -> list[AttributeModifier]:
        return self._map[attr]

    def set(self, attribute: Attribute, modifier: AttributeModifier) -> bool:
        if attribute not in self._map:
            self._map[attribute] = []
        if modifier in self._map[attribute]:
            return False
        if len(self._map[attribute]) == 0:
            self._map[attribute] = []
        self._map[attribute].append(modifier)
        return True

    def setNew(
        self,
        attribute: Attribute,
        uuid: UUID | None = None,
        type: Literal['+'] | Literal['+*'] | Literal['*']
        | AttributeModifierType = "+",
        amount: int | float = 0,
    ) -> AttributeModifier:
        _t = {
            "+": AttributeModifierType.ADDITION,
            "+*": AttributeModifierType.MULT_BASE,
            "*": AttributeModifierType.MULT_TOTAL
        }[type] if not isinstance(type, AttributeModifierType) else type
        modifier = AttributeModifier(uuid or uuid4(), _t, amount)
        self.set(attribute, modifier)
        return modifier

    def _put(
        self,
        attribute: Attribute,
        uuid: UUID | None = None,
        type: Literal['+'] | Literal['+*'] | Literal['*']
        | AttributeModifierType = "+",
        amount: int | float = 0,
    ) -> "ModifierMap":
        self.setNew(attribute, uuid, type, amount)
        return self

    def get(self, attr: Attribute, id: UUID) -> AttributeModifier:
        _l = [_m for _m in self.get_modifiers(attr) if _m.id is id]
        if len(_l) == 0:
            return self.setNew(attr, uuid=id)
        return _l[0]

    def get_modifiers(self, attr: Attribute) -> list[AttributeModifier]:
        if attr not in self._map:
            self._map[attr] = []
        return self._map[attr]

    def has(self, attr: Attribute, id: UUID | None = None) -> bool:
        if id is None:
            return attr in self._map
        return attr in self._map and id in {_m.id for _m in self._map[attr]}

    def __repr__(self) -> str:
        return repr(self._map)
