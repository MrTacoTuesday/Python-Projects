from .attribute import Attribute
from .attribute_handler import AttributeHandler
from .attributes import Attributes
from .modifier_map import ModifierMap


class AttributeMap:

    def __init__(
        self,
        attr_map:
        "AttributeMap | dict[Attribute, AttributeHandler] | None" = None):
        self._map: dict[Attribute, AttributeHandler] = {}
        if isinstance(attr_map, dict):
            for attr, handler in attr_map.items():
                if not isinstance(attr, Attribute):
                    continue
                if not isinstance(handler, AttributeHandler):
                    continue
                self._map[attr] = handler
        elif isinstance(attr_map, AttributeMap):
            self._map = attr_map._map

    def __getitem__(self, attr: Attribute) -> AttributeHandler:
        return self._map[attr]

    def set(self, handler: AttributeHandler) -> bool:
        if handler.attribute in self._map:
            return False
        self._map[handler.attribute] = handler
        return True

    def setNew(self, attribute: Attribute) -> AttributeHandler:
        handler = AttributeHandler(attribute)
        self.set(handler)
        return handler

    def get(self, attr: Attribute) -> AttributeHandler:
        if attr not in self._map:
            return self.setNew(attr)
        return self._map[attr]

    def has(self, attr: Attribute) -> bool:
        return attr in self._map

    def clear_listeners(self):
        for handler in self._map.values():
            handler.clear_listeners()

    def apply_modifiers(self, modifiers: ModifierMap):
        for handler in self._map.values():
            if not modifiers.has(handler.attribute):
                continue
            _m = modifiers.get_modifiers(handler.attribute)
            for m in _m:
                handler.add_modifier(m)

    def remove_modifiers(self, modifiers: ModifierMap):
        for handler in self._map.values():
            _m = modifiers.get_modifiers(handler.attribute)
            for m in _m:
                handler.remove_modifier(m)
