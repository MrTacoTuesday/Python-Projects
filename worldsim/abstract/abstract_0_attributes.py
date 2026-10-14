from enum import Enum, IntEnum
from math import inf, prod
from typing import Any, Self
from uuid import UUID, uuid4

class AttributeDefinition:
    id: str
    min: float
    base: float
    max: float

    def __init__(self, id: str, base: float | None, max: float | None = None, min: float | None = None) -> None:
        self.id = id
        self.min = min or 0
        self.base = base or 0
        self.max = inf if max is None else max
        assert self.max >= self.base
        assert self.min <= self.base

    def clamp(self, value: float) -> float:
        return max(self.min, min(value, self.max))

    @property
    def current(self) -> float:
        return self._current
    @current.setter
    def current(self, value: float):
        self._current = self.clamp(value)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'min': self.min,
            'base': self.base,
            'max': self.max,
        }
    
    @classmethod
    def from_dict(cls, dict: dict[str, Any]) -> Self:
        return cls(**dict)

class AttributeModifier:
    class Operation(IntEnum):
        ADD = 0b0
        ADD_MUL = 0b1
        MUL = 0b10

    id: UUID
    operation: AttributeModifier.Operation
    value: float

    def __init__(self, id: UUID, value: float, operation: AttributeModifier.Operation, layer: int = 0) -> None:
        self.id = id
        self.layer = layer
        self.operation = operation
        self.value = value

    def __hash__(self) -> int:
        return self.id.__hash__()

class Attribute:

    definition: AttributeDefinition
    _modifiers: set[AttributeModifier]

    _value: float = 0
    _dirty: bool = True

    def __init__(self, definition: AttributeDefinition) -> None:
        self.definition = definition
        self._modifiers = set()

    def recalculate(self) -> None:
        value = self.definition.base

        layers: dict[int, tuple[list[float], list[float]]] = {}
        for modifier in self._modifiers:
            layers.setdefault(modifier.layer, ([],[]))
            layers[modifier.layer][modifier.operation].append(modifier.value)

        for layer in sorted(layers):
            value += sum(layers[layer][AttributeModifier.Operation.ADD])
            value *= sum(layers[layer][AttributeModifier.Operation.ADD_MUL], 1)
            value *= prod(layers[layer][AttributeModifier.Operation.MUL])

        self._value = value
        self._dirty = False

    def __iadd__(self, other: AttributeModifier | int | float):
        if isinstance(other, int|float):
            other = AttributeModifier(uuid4(), other, AttributeModifier.Operation.ADD)
        self._modifiers.add(other)
        self._dirty = True

    def __isub__(self, other: UUID | AttributeModifier | int | float):
        if isinstance(other, int|float):
            self += -other
        elif isinstance(other, UUID):
            for m in filter(lambda x: x.id == other, self._modifiers):
                self._modifiers.discard(m)
                self._dirty = True
        else:
            self._modifiers.discard(other)
            self._dirty = True

    def __imul__(self, other: int | float):
        self += AttributeModifier(uuid4(), other, AttributeModifier.Operation.MUL)
            

    @property
    def rawvalue(self) -> float:
        if self._dirty:
            self.recalculate()
        return self._value

    @property
    def value(self) -> float:
        return self.definition.clamp(self.rawvalue)



class Attributes(Enum, AttributeDefinition): # base is adult average/median values
    MAX_HYDRATION = ('capacity/water', 0.7) # L H2O (4h reserve)
    DIGESTIVE_CAPACITY = ('capacity/food', 0.8) # kg (4h reserve)
    OXYGEN_CAPACITY = ('capacity/oxygen', 110) # L O2
    MAX_STAMINA = ('capacity/energy', 60) # kcal
    RESTING_RESPIRATORY_RATE = ('intake/oxygen', 20) # L O2 / h
    METABOLIC_RATE = ('body/metabolism', 75) # kcal/h

    # caloric_mass [kg] = 0.000164 * metabolic_rate * 1h
    #   stamina += caloric_mass * 6125
    #   digestive_mass [kg] -= caloric_mass
    #   if digestive_mass < 0:
    #     weight -= -digestive_mass
    #     digestive_mass = 0

    # lose water via sweat (temp cooling), urination, blood loss, etc

    # when stamina gets too low, rest is needed
    # when mental energy gets too low or stamina gets extremely low, sleep is needed

    ENDURANCE = ('body/endurance', 1) # TODO: research starting value # greater endurance reduces energy expenses

    MAX_VITALITY = ('body/health', 0) # TODO # general healthiness
    IMMUNE_SYSTEM_HEALTH = ('body/immune-system-health', 0) # TODO # will help with probability-based fighting of disease

    WEIGHT = ('body/weight', 63) # kg
    HEIGHT = ('body/height', 1.65) # m

    LEARNING_RATE = ('brain/learning-rate', 1) # TODO

    P_ENERGY = ('personality/energy', 0.5, 1) # Introversion (0) vs. Extroversion (1)
    P_PERCEPTION = ('personality/perception', 0.5, 1) # Sensing vs. Intuition
    P_DECISION = ('personality/decision', 0.5, 1) # Thinking vs. Feeling
    P_INTERACTION = ('personality/interaction', 0.5, 1) # Judging vs. Perceiving
    P_IDENTITY = ('personality/identity', 0.5, 1) # Assertive vs. Turbulent


    STAT_DECAY_RATE = ('body/decay', 0) # TODO # Stat deterioration rate past adulthood


from typing import Final
from uuid import UUID, uuid4


class Unit:


    id: Final[UUID]
    genetics: None

    def __init__(self, id: UUID | None = None) -> None:
        self.id = id or uuid4()