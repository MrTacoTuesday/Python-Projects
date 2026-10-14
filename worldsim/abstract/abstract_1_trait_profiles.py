
from dataclasses import dataclass, field
from enum import Enum, auto
from math import inf
from typing import Final
from uuid import UUID, uuid3, uuid4


#TRAIT_NAMESPACE_ID = UUID("20997e27-d28c-4c82-8628-b4401f677f88")

class Sex(Enum):
    MALE = auto()
    FEMALE = auto()
    ASEXUAL = auto()

@dataclass
class ReproductiveSystemState:
    __slots__ = ('sex',)
    sex: Final[Sex]

    @property
    def sex_of_mate(self) -> Sex:
        match self.sex:
            case Sex.ASEXUAL:
                return Sex.ASEXUAL
            case Sex.MALE:
                return Sex.FEMALE
            case Sex.FEMALE:
                return Sex.MALE

@dataclass
class Trait[_Type: int | float = float]:
    base: _Type
    efficiency: float = 1
    multiplier: float = 1

    Type: type[_Type] = field(init=False)

    def post_init(self, *args, **kwargs):
        self.Type = self.base.__class__

    @property
    def value(self) -> _Type:
        return self.Type(self.base * self.efficiency * self.multiplier)

    def condense(self) -> None:
        self.base = self.value
        self.efficiency = 1
        self.multiplier = 1

@dataclass
class BoundTrait[_Type: int | float = float](Trait[_Type]):
    minimum: Trait[int | float] = field(default_factory=lambda: Trait(0))
    maximum: Trait[int | float] = field(default_factory=lambda: Trait(inf))

    @property
    def value(self) -> _Type:
        return self.Type(max(self.minimum.value, min(super().value, self.maximum.value)))

@dataclass
class HealthState:
    ...

@dataclass
class SleepState:
    ...

@dataclass
class MetabolismState:
    oxygen_reserve_liters: BoundTrait
    energy_reserve_kcal: BoundTrait
    water_reserve_liters: BoundTrait


@dataclass
class DigestiveSystemState:
    ...

@dataclass
class RespiratorySystemState:
    lung_capacity_liters: BoundTrait

    respiration_rate_liters: BoundTrait
    alveoli_efficiency: Trait
    ...

@dataclass
class MusculoskeletalSystemState:
    ...

@dataclass
class CardiovascularSystemState:
    ...

@dataclass
class ImmuneSystemState:
    ...

@dataclass
class Body:
    age_hours: Trait[int]

    height_cm: Trait
    mass_kg: Trait

    health: HealthState
    sleep: SleepState

    cardiovascular_system: CardiovascularSystemState
    musculoskeletal_system: MusculoskeletalSystemState
    reproductive_system: ReproductiveSystemState
    digestive_system: DigestiveSystemState
    respiratory_system: RespiratorySystemState
    immune_system: ImmuneSystemState

    metabolism: MetabolismState

@dataclass
class Personality:
    energy: BoundTrait # Introversion (0) vs. Extroversion (1)
    perception: BoundTrait # Sensing vs. Intuition
    decision: BoundTrait # Thinking vs. Feeling
    interaction: BoundTrait # Judging vs. Perceiving
    identity: BoundTrait # Assertive vs. Turbulent

@dataclass
class Skill:
    ...
@dataclass
class Memory:
    ...
@dataclass
class Concept:
    ...
@dataclass
class Belief:
    ...
@dataclass
class Goal:
    ...

@dataclass
class Mind:
    personality: Personality
    skills: dict[Skill, float]
    memories: list[Memory]
    beliefs: dict[Concept, Belief]
    current_goal: Goal | None

@dataclass
class Relationship:
    ...

@dataclass
class Item:
    ...

@dataclass
class InventorySlot:
    layers: list[Item]
    def subslots(self) -> list[InventorySlot]:
        ...

@dataclass
class ContainerItem(Item):
    ...

@dataclass
class BipedInventory:
    head: InventorySlot
    neck: InventorySlot
    back: InventorySlot
    shoulders: InventorySlot
    torso: InventorySlot
    arms: InventorySlot
    hands: InventorySlot
    waist: InventorySlot
    legs: InventorySlot
    feet: InventorySlot
    ...
    # just ideas

@dataclass
class TilePosition:
    x: int
    z: int

@dataclass
class GridPosition:
    tile: TilePosition
    x: float # [0-1)
    z: float # [0-1)

@dataclass
class Job:
    ...

@dataclass
class SocialState:
    household_id: UUID | None
    culture_ids: set[UUID]
    language_ids: set[UUID]
    relationships: dict[UUID, Relationship]

@dataclass
class EconomicState:
    job: Job | None
    inventory: BipedInventory
    money: float
    home_cell: GridPosition
