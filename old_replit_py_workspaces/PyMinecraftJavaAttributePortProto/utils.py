from typing import TypeVar, Callable


"""class Selfed:
	Self = TypeVar("Selfed.Self", bound="Selfed")

	def __init_subclass__(cls: Self):
		cls.Self = TypeVar(f"{cls.__qualname__}.Self", bound=cls.__qualname__)"""

_R = TypeVar("ReturnType")
_T = TypeVar("InputType")
_T2 = TypeVar("InputType2")

Action = Callable[[], None]

Supplier = Callable[[], _R]

Function = Callable[[_T], _R]

BiFunction = Callable[[_T, _T2], _R]

Consumer = Callable[[_T], None]

BiConsumer = Callable[[_T, _T2], None]
