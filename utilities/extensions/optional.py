from collections.abc import Callable
from typing import Optional



def ifPresent[X, R1, R2](self: Optional[X], transform: Callable[[X], R1], otherwise: R2 = None) -> Optional[R1]:
    return otherwise if self is None else transform(self)

def ifEmpty[X, R](self: Optional[X], *, default: R = None, factory: Callable[[], R] = None) -> X | R:
    assert (default is None) != (factory is None), "Must provide either default or factory"
    if self is None:
        return default if factory is None else factory()
    return self