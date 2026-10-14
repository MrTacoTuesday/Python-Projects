from dataclasses import dataclass
from enum import Enum, StrEnum, auto


### LINK-LAZY HANDLING ###

class LazyAssignmentError(PermissionError): ...

class _unassigned: 
    def __repr__(self) -> str:
        return '<unassigned>'
unassigned = _unassigned()
del _unassigned


@dataclass
class Lazy[T]:
    _value_map: dict[object, T] = {}

    def __set__(self, instance, value: T):
        instance_value = self._value_map.get(instance, unassigned)
        if instance_value is unassigned:
            self._value_map[instance] = value
        elif self._value_map is value:
            pass
        else:
            raise LazyAssignmentError()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._value_map[instance]


### LANGUAGE SYSTEMS ###

class SpeechAction(StrEnum):
    Identify = auto()
    Inform = auto()
    Request = auto()
    Offer = auto()
    Refuse = auto()
    Promise = auto()
    Ask = auto()
    Warn = auto()
    Greet = auto()
    Farewell = auto()
    Thank = auto()
    Apologize = auto()
    Command = auto()
    Affirm = auto()
    Deny = auto()
    RequestPermission = auto()

class SemanticRole(StrEnum):
    Agent = auto()
    Recipient = auto()
    Patient = auto()
    Experiencer = auto()
    Instrument = auto()
    Location = auto()
    Source = auto()
    Destination = auto()

class WordPart(StrEnum):
    Subject = auto()
    Verb = auto()
    Object = auto()



class ConstituentOrder(tuple[WordPart,WordPart,WordPart], Enum):
    ## Enum treats assignment as args to base type, so a non-tuple iterable is needed as tuple(iterable) arg
    SVO = [WordPart.Subject, WordPart.Verb, WordPart.Object]
    SOV = [WordPart.Subject, WordPart.Object, WordPart.Verb]
    VSO = [WordPart.Verb, WordPart.Subject, WordPart.Object]
    VOS = [WordPart.Verb, WordPart.Object, WordPart.Subject]
    OVS = [WordPart.Object, WordPart.Verb, WordPart.Subject]
    OSV = [WordPart.Object, WordPart.Subject, WordPart.Verb]