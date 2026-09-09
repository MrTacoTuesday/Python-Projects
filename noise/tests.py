from collections.abc import Callable
from datetime import datetime
from typing import Any

from noise.perlin import Perlin
from noise.hashrandom import HashRandom, SeededHash


def _wrapper[T : Callable](fn: T) -> T:
    name: str = fn.__name__.replace('_', ' ').title().__repr__()
    def call(*args, **kwargs) -> Any:
        t: datetime = datetime.now()
        print(f'Starting {name} at {t}')
        try:
            result = fn(*args, **kwargs)
        except:
            print(f'Failed {name}!')
            raise
        t2: datetime = datetime.now()
        print(f'Cleared {name} at {t2} (completed in {t2-t})')
        return result
    return call # type: ignore

@_wrapper
def test_seededhash() -> None:

    hasher = SeededHash()
    print(hasher)
    print(hasher.process(None, 3.7, 255, {}, [], (), set(), complex(4, 3.14), frozenset(), {():()}, object()))
    for _ in range(3): print(hasher.nextstate())



@_wrapper
def run_all_tests() -> None:
    test_seededhash()



if __name__ == '__main__':
    run_all_tests()