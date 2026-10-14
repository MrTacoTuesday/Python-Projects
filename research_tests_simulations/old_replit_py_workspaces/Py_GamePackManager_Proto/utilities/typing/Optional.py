from collections.abc import Callable
from types import FunctionType, WrapperDescriptorType
from typing import Any, Generic, Type, TypeVar, final

_T = TypeVar("_T")
_K = TypeVar("_K")


@final
class Optional(Generic[_T]):

    ____PROTOTYPE____: Type = Any

    def __init__(self, *args, _a7df29ae10f3d8c3cf12b9=None, **kwargs) -> None:
        self.____prototype____ = self.____PROTOTYPE____
        if _a7df29ae10f3d8c3cf12b9:
            self.____mirror____ = None
        else:
            self.____mirror____ = self.____prototype____(*args, **kwargs)

    @classmethod
    def Empty(cls):
        return Optional[cls.____PROTOTYPE____](_a7df29ae10f3d8c3cf12b9=True)

    @classmethod
    def assign(cls, __value: _T | None) -> "Optional[_T]":
        slf = Optional[cls.____PROTOTYPE____].Empty()
        slf.____mirror____ = __value
        return slf

    @classmethod
    def trying(cls,
               __action: Callable[[], _T | None],
               __failure: _T | None = None) -> "Optional[_T]":
        try:
            return Optional[cls.____PROTOTYPE____].assign(__action())
        except Exception:
            return Optional[cls.____PROTOTYPE____].assign(__failure)

    def orElse(self, alternative: _K) -> _T | _K:
        if self.____mirror____:
            return self.____mirror____
        else:
            return alternative

    def obtain(self) -> _T | None:
        return self.____mirror____

    def forceCast(self) -> _T:
        if self.____mirror____:
            return self.____mirror____
        else:
            raise Exception("Optional has no value")

    def isPresent(self) -> bool:
        return self.____mirror____ is not None

    def ifPresent(self, __action: Callable[[_T], _K],
                  returns: Type[_K]) -> "Optional[_K]":
        if self.____mirror____:
            return Optional[returns].assign(__action(self.____mirror____))
        else:
            return Optional[returns].Empty()

    def __getattribute__(self, __name: str) -> Any:
        if __name in [
                "____prototype____", "____PROTOTYPE____", "____mirror____",
                "orElse", "isPresent", "Empty", "assign", "obtain",
                "ifPresent", "trying", "forceCast"
        ]:
            return super().__getattribute__(__name)
        elif self.____mirror____ is None:
            o = self.____prototype____.__dict__.get(__name)
            if isinstance(o, (FunctionType, WrapperDescriptorType)):
                return (lambda *args, **kwargs: None)
            else:
                return None
        else:
            return self.____mirror____.__getattribute__(__name)

    def __class_getitem__(cls, item: Type[_T]):
        cls.____PROTOTYPE____ = item
        return cls

    def __repr__(self) -> str:
        return f"""Optional[{
            self.____prototype____.__name__
        }]({self.____mirror____ or ""})"""
