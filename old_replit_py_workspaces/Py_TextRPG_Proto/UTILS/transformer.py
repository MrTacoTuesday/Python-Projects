from collections.abc import Callable
from typing import TypeVar

_T = TypeVar("_T")
_R = TypeVar("_R")
Transformer = Callable[[_T], _R]
