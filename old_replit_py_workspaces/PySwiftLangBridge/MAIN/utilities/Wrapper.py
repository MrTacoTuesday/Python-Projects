import types
from collections.abc import Callable
from types import UnionType
from typing import Any, Generic, Type, TypeVar

_Bound = TypeVar("_Bound")


class Wrapper(Generic[_Bound]):

    ____PROTOTYPE____: Type[_Bound] = Any

    def __init__(self, *args, **kwargs) -> None:
        self.____prototype____ = self.____PROTOTYPE____
        try:
            self.____mirror____ = self.____prototype____(*args, **kwargs)
        except Exception as e:
            raise e

    @classmethod
    def Bound(cls) -> Type[_Bound]:
        return cls.____PROTOTYPE____

    @classmethod
    def isBoundNoneType(cls) -> bool:
        return (cls.____PROTOTYPE____ is None
                or isinstance(cls.____PROTOTYPE____, types.NoneType))

    @classmethod
    def isBoundUnionType(cls) -> bool:
        try:
            return (cls.____PROTOTYPE____.__qualname__ == "Union")
        except Exception:
            try:
                return isinstance(cls.____PROTOTYPE____, UnionType)
            except Exception:
                return False

    @classmethod
    def ____test____(cls, __instance__: _Bound) -> bool:
        if cls.isBoundNoneType():
            return __instance__ is None
        return isinstance(__instance__, cls.____PROTOTYPE____)

    @classmethod
    def assign(cls, __value: _Bound) -> "Wrapper[_Bound]":
        if not cls.____test____(__value):
            raise TypeError(f"{__value} is not a {cls.____PROTOTYPE____}")
        slf = cls.__new__(Wrapper[cls.____PROTOTYPE____])
        slf.____prototype____ = cls.____PROTOTYPE____
        slf.____mirror____ = __value
        return slf

    @classmethod
    def trying(cls, __action: Callable[[], _Bound],
               __failure: _Bound) -> "Wrapper[_Bound]":
        try:
            return Wrapper[cls.____PROTOTYPE____].assign(__action())
        except Exception as e:
            if (__failure is not None
                    and cls.____PROTOTYPE____ is not type(None)):
                return (Wrapper[cls.____PROTOTYPE____].assign(__failure))
            else:
                raise e

    def obtain(self) -> _Bound:
        return self.____mirror____

    def ____wrapper_subclass_attributes____(self) -> Any:
        raise NotImplementedError()

    def ____wrapper_attributes____(self) -> list[str]:
        return [
            "____PROTOTYPE____",
            "Bound",
            "isBoundNoneType",
            "isBoundUnionType",
            "__class_repr__",
            "____mirror____",
            "____prototype____",
            "____wrapper_subclass_attributes____",
            "obtain",
            "assign",
            "trying",
        ]

    def __getattribute__(self, __name: str) -> Any:
        if __name == "____wrapper__init__":
            return super().__getattribute__("__init__")
        elif __name == "____wrapper__class_getitem__":
            return super().__getattribute__("__class_getitem__")
        elif __name == "____wrapper__repr__":
            return super().__getattribute__("__repr__")
        elif (__name == "____wrapper_attributes____"
              or __name in self.____wrapper_attributes____()):
            return super().__getattribute__(__name)
        try:
            return self.____wrapper_subclass_attributes____()
        except Exception:
            return self.____mirror____.__getattribute__(__name)

    @classmethod
    def __class_getitem__(cls, item: Type[_Bound]):
        cls.____PROTOTYPE____ = item
        return cls

    @classmethod
    def __class_repr__(cls) -> str:
        name = ""
        if cls.isBoundUnionType() or cls.isBoundNoneType():
            name = cls.____PROTOTYPE____.__repr__()
        else:
            name = cls.____PROTOTYPE____.__name__
        return f"{cls.__name__}[{name}]"

    def __repr__(self) -> str:
        return f"{self.__class_repr__()}({self.____mirror____})"
