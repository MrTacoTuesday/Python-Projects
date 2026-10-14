from uuid import UUID

from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.UTILS.listener import Listener
from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.UTILS.transformer import Transformer

from .attribute import Attribute
from .attribute_modifier import AttributeModifier
from .attribute_modifier_type import AttributeModifierType


class AttributeHandler:

    def __init__(self, attribute: Attribute):
        self.attribute: Attribute = attribute
        self.modifiers: list[AttributeModifier] = []
        self.listeners: list[Listener[AttributeHandler]] = []
        self._value: float = attribute.baseValue
        self.flag: bool = False

    def _recalc(self):
        v1, v2, v3 = self.attribute.baseValue, 0, 1
        for modifier in self.modifiers:
            if modifier.type == AttributeModifierType.ADDITION:
                v1 += modifier.amount
            elif modifier.type == AttributeModifierType.MULT_BASE:
                v2 += modifier.amount
            elif modifier.type == AttributeModifierType.MULT_TOTAL:
                v3 *= modifier.amount
        self._value = v1 * (1 + v2) * v3
        self.flag = False
        self.notify_listeners()

    def add_modifier(self, modifier: AttributeModifier):
        if self.modifiers.count(modifier):
            return
        self.modifiers.append(modifier)
        self.flag = True

    def get_modifier(self, uuid: UUID) -> AttributeModifier | None:
        return next((x for x in self.modifiers if x.id == uuid), None)

    def remove_modifier(self, modifier: AttributeModifier | UUID):
        m = modifier if not isinstance(modifier,
                                       UUID) else self.get_modifier(modifier)
        if not m:
            return
        self.modifiers.remove(m)
        self.flag = True

    def update_modifier(self, uuid: UUID, transform: Transformer[float,
                                                                 float]):
        m = self.get_modifier(uuid)
        if not m:
            return
        m.amount = transform(m.amount)
        self.flag = True

    def add_listener(self, listener: "Listener[AttributeHandler]"):
        self.listeners.append(listener)

    def remove_listener(self, listener: "Listener[AttributeHandler]"):
        self.listeners.remove(listener)

    def notify_listeners(self):
        for listener in self.listeners:
            listener(self)

    def clear_listeners(self):
        self.listeners = []

    @property
    def value(self) -> float:
        if self.flag:
            self._recalc()
        return self._value
