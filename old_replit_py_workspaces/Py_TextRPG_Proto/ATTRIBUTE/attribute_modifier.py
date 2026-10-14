from uuid import UUID

from .attribute_modifier_type import AttributeModifierType


class AttributeModifier:

    def __init__(self, id: UUID, type: AttributeModifierType,
                 amount: float | int):
        self.id: UUID = id
        self.type: AttributeModifierType = type
        self.amount: float = float(amount)

    def is_same_modifier(self, id: UUID) -> bool:
        return self.id == id
