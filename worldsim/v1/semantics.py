from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import TypeAlias
from uuid import uuid4

from .ids import ConceptID, FrozenIDSet, PersistentID


class SemanticRole(StrEnum):
    AGENT = auto()
    PATIENT = auto()
    RECIPIENT = auto()
    EXPERIENCER = auto()
    INSTRUMENT = auto()
    LOCATION = auto()
    SOURCE = auto()
    DESTINATION = auto()


class SpeechAct(StrEnum):
    INFORM = auto()
    REQUEST = auto()
    ASK = auto()
    OFFER = auto()
    REFUSE = auto()
    PROMISE = auto()
    WARN = auto()
    COMMAND = auto()
    GREET = auto()


@dataclass(frozen=True, slots=True)
class Concept:
    key: str
    category: str
    id: ConceptID = field(default_factory=uuid4)


SemanticValue: TypeAlias = PersistentID | int | float | str


@dataclass(frozen=True, slots=True)
class SemanticArgument:
    role: SemanticRole
    value: SemanticValue


@dataclass(frozen=True, slots=True)
class Proposition:
    predicate_id: ConceptID
    arguments: tuple[SemanticArgument, ...] = ()
    negated: bool = False


@dataclass(frozen=True, slots=True)
class CommunicativeIntent:
    speech_act: SpeechAct
    speaker_id: PersistentID
    listener_ids: FrozenIDSet[PersistentID] = field(
        default_factory=FrozenIDSet[PersistentID]
    )
    content: Proposition | None = None
    urgency: float = 0.0
    politeness: float = 0.5

    def __post_init__(self) -> None:
        if not 0.0 <= self.urgency <= 1.0:
            raise ValueError("urgency must be between 0.0 and 1.0")
        if not 0.0 <= self.politeness <= 1.0:
            raise ValueError("politeness must be between 0.0 and 1.0")
