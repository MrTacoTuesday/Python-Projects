from typing import Any, Type

from typing_extensions import Self, TypeVar


class __ObjectMeta(type):

    def __new__(cls: Type[Self], name: str, bases: tuple[Type, ...],
                namespace: dict[str, Any]) -> Self:
        _Slf = super().__new__(cls, name, bases, namespace)
        cls.Self = _Slf
        _Slf.Self = _Slf
        return _Slf

    def __repr__(self: Self) -> str:
        return f"<Object class '{self.__name__}'>"

    @property
    def Super(self: Self) -> "Type[Object]":
        for base in self.__bases__:
            if issubclass(base, Object):
                return base
        return Object


class Object(metaclass=__ObjectMeta):
    
    def toString(self: Self) -> "String":
        return String(self)

    def __repr__(self: Self) -> str:
        return self.toString()

class String(str, Object):

    @staticmethod
    def fromPrimitive(value: str) -> "String":
        return String(value)

    
    def toString(self: Self) -> "String":
        return self

print(String.Super)