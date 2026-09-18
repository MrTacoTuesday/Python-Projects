from collections.abc import Callable
from datetime import datetime
import random
import statistics
import time
from types import MethodType
from typing import Any
from typing_extensions import Self

from noise.hashrandom import HashRandom, SeededHash
from utilities import debug

class Wrapper[T: Callable]:
    __function__: T
    __kwargs__: dict[str, Any]

    def __new__(cls, fn: T, **kwargs: Any) -> Self:
        self = super().__new__(cls)
        self.__function__ = fn
        self.__kwargs__ = kwargs
        return self

    @property
    def function_name(self) -> str:
        return self.__function__.__name__.__repr__()

    def on_before(self, args: tuple[Any, ...], kwargs: dict[str, Any], start_time: datetime) -> None:
        """
        Hook that gets called just before the target function is called.
        In subclasses, call super BEFORE your implementation for best results:
            ```python
            def on_before(args, kwargs, start_time):
                super().on_before(args, kwargs, start_time)
                ... # subclass implementation here
            ```
        """
        debug(f'Starting {self.function_name} at {start_time}')

    def on_fail(self, args: tuple[Any, ...], kwargs: dict[str, Any], start_time: datetime, fail_time: datetime, exception: Exception) -> Any:
        """
        Hook that gets called when the target function raises an exception. Return a default value, otherwise reraise the exception.
        In subclasses, call super AFTER your implementation for best results:
            ```python
            def on_fail(self, args, kwargs, start_time, fail_time, exception):
                if some_condition:
                    raise exception from None # could raise here if you wanted
                elif dont_raise:
                    return default_value
                return super().on_fail(self, args, kwargs, start_time, fail_time, exception) # raises
            ```
        """
        debug(f'Failed {self.function_name} at {fail_time}!')
        raise exception

    def on_success(self, args: tuple[Any, ...], kwargs: dict[str, Any], start_time: datetime, succeed_time: datetime, result: Any) -> None:
        """
        Hook that gets called when the target function successfully executes.
        In subclasses, call super BEFORE your implementation for best results:
            ```python
            def on_success(self, args, kwargs, start_time, succeed_time, result):
                super().on_success(self, args, kwargs, start_time, succeed_time, result)
                ... # print('Hooray! We did it!')
            ```
        """
        debug(f'Succeeded {self.function_name} with result `{result}` at {succeed_time} (took {(succeed_time-start_time).total_seconds()}s)')

    def on_after(self, args: tuple[Any, ...], kwargs: dict[str, Any], start_time: datetime, finish_time: datetime, result: Any) -> None:
        """
        Hook that gets called after the target function is called, no matter success or fail.
        In subclasses, call super AFTER your implementation for best results:
            ```python
            def on_after(self, args, kwargs, start_time, succeed_time, result):
                ... # do something
                super().on_after(self, args, kwargs, start_time, succeed_time, result)
            ```
        """
        debug(f'Exited {self.function_name} with result `{result}` at {finish_time} (took {(finish_time-start_time).total_seconds()}s)')
        time.sleep(2)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Calls the wrapped function, injecting the event hooks. 
        This method should not be overridden.
        """
        self.on_before(args, kwargs, start_time := datetime.now())
        try:
            result = self.__function__(*args, *kwargs)
            self.on_success(args, kwargs, start_time, finish_time := datetime.now(), result)
            return result
        except Exception as exception:
            finish_time = datetime.now()
            result = self.on_fail(args,kwargs,start_time, finish_time, result := exception)
            return result
        finally: # allows for potential re-raise of the except block while still calling on_after
            self.on_after(args, kwargs,start_time,finish_time,result) # pyright: ignore[reportPossiblyUnboundVariable]

def defaultkey(x: Any) -> Any:
    return x

def _uniqueness_test(fn: MethodType, *, N: int = 10_000, key: Callable[[Any], Any]=defaultkey):
    uniques = set()
    duplicates = 0
    print(f'\tChecking {N:,} calls to {fn.__qualname__} for uniqueness...')
    for _ in range(N): 
        if (i := key(fn())) in uniques:
            duplicates += 1
        else:
            uniques.add(i)
    uniques = len(uniques)+(duplicates>>1)
    print(f'\tCheck complete. {uniques:,}/{N:,} ({uniques/N:0.2%}) unique values produced')

@Wrapper
def seededhash_capability_test() -> None:

    hasher = SeededHash()
    print(hasher)
    print(hasher.process(None, 3.7, 255, {}, [], (), set(), complex(4, 3.14), frozenset(), {():()}, object()))
    _uniqueness_test(hasher.nextstate, N=1_000_000, key=bytes)
    

@Wrapper
def random_method_statistics_test[T: random.Random](cls: type[T], N: int = 10_000) -> None:
    rng = cls(cls.__qualname__*10)

    print(f'Targeting Generator {cls.__qualname__}:')
    print(  f'\t{rng}')

    print(f'population (N={N:,}) stats:')

    population = [0.0]*N
    k = (N+999)//1_000 # 0.1% of N

    for i in range(N):
        if not (i % k): print(  f'\t(generating {i/N:0.1%})', end='\r')
        population[i] = rng.random()
    print(  '\t(generated 100%, getting stats...)')
    print(  '\tpop. mean:       ', statistics.mean(population))
    print(  '\tpop. variance:   ', statistics.variance(population, 0.5))

    n = (N+9)//10
    print(f'sample (n={n:,}):')

    sample = random.sample(population, n)
    print(  '\t(generated 100%, getting stats...)')
    print(  '\tsample mean:     ', statistics.mean(sample))
    print(  '\tsample variance: ', statistics.variance(sample, 0.5))


@Wrapper
def hashrandom_capability_test() -> None:
    #random_method_statistics_test(random.Random, 1_000_000)
    #random_method_statistics_test(HashRandom, 1_000_000)
    hashrandom_getrandbits_test()

@Wrapper
def hashrandom_getrandbits_test() -> None:
    print(rng := HashRandom("HashRandom"*32, size=4))
    print(bytes(rng)[0:3].hex())
    print(tuple(rng.getrandbits(1) for _ in range(32)))
    print(rng)

@Wrapper
def run_all_tests() -> None:
    print(rng := HashRandom("HashRandom"*32, size=4))
    print(tuple(rng.random() for _ in range(32)))
    print(rng)
    #seededhash_capability_test()
    hashrandom_capability_test()



if __name__ == '__main__':
    run_all_tests()