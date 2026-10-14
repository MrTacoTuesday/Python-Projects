from collections.abc import Callable, Iterable
from typing import TypeVar

_T = TypeVar("_T")
Listener = Callable[[_T], None | Iterable[None]]
