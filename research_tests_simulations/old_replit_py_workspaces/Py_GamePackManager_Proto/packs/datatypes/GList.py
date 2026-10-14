from collections.abc import Iterable
from typing import Any, Type, TypeVar

_T = TypeVar('_T')


class GList(list[_T]):

    ____element____: Type = Any

    @classmethod
    def fromdata(cls, data: Any) -> "GList[_T]":
        if (isinstance(data, GList)
                and issubclass(data.____element____, cls.____element____)):
            return data
        elif isinstance(data, list):
            if not all(isinstance(x, cls.____element____) for x in data):
                cls.elementError()
            return GList[cls.____element____](data)
        elif isinstance(data, str):
            return GList[cls.____element____]([data])
        else:
            raise TypeError(f"Invalid {cls.__class_repr__()}")

    def __class_getitem__(cls, item: Type[_T]):
        cls.____element____ = item
        return cls

    @classmethod
    def __class_repr__(cls) -> str:
        return f"GList[{cls.__element_repr__()}]"

    @classmethod
    def __element_repr__(cls) -> str:
        return cls.____element____.__class__.__name__

    @classmethod
    def elementError(cls):
        raise TypeError(
            f"{cls.__class_repr__()} can only contain {cls.__element_repr__()}"
        )

    def __init__(self, __iterable: Iterable[_T]):
        if not all(isinstance(x, self.____element____) for x in __iterable):
            self.elementError()
        super().__init__(__iterable)
