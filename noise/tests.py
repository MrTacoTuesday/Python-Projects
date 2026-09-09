from collections.abc import Callable
from datetime import datetime
from typing import Any


MAIN = (__name__ == '__main__')




try:
    from perlin import Perlin
    from hashrandom import HashRandom, SeededHash
except:
    from .perlin import Perlin
    from .hashrandom import HashRandom, SeededHash


def _wrapper[T : Callable](fn: T) -> T:
    name = fn.__name__.replace('_', ' ').title().__repr__()
    def call(*args, **kwargs) -> Any:
        t = datetime.now()
        print(f'Running {name} at {t}')
        try:
            return fn(*args, **kwargs)
        finally:
            t2 = datetime.now()
            print(f'Completed {name} at {t2} (completed in {t2-t})')
    return call # type: ignore

@_wrapper
def test_seededhash():

    empty = SeededHash()
    print(empty)
    empty.process(None, 3.7, 255, {}, [], (), set(), complex(4, 3.14), frozenset(), {():()}, object())



@_wrapper
def run_all_tests():
    test_seededhash()



if MAIN:
    run_all_tests()