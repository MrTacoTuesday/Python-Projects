from collections.abc import Container
from dataclasses import dataclass, field
from math import inf, nan

if __name__ == '__main__':
    from epsilon import Epsilon
else:
    from .epsilon import Epsilon

_RealLike = int | float

@dataclass(frozen=True, match_args=True, slots=True)
class RealRange(Container[_RealLike]):
    min: _RealLike
    max: _RealLike
    excludes_min: bool = field(default=False, kw_only=True)
    excludes_max: bool = field(default=False, kw_only=True)
    epsilon: Epsilon = field(default=Epsilon.FloatingPoint, kw_only=True)

    @property
    def truemin(self) -> _RealLike:
        return (self.min + self.epsilon) if self.excludes_min else self.min

    @property
    def truemax(self) -> _RealLike:
        return (self.max - self.epsilon) if self.excludes_max else self.max

    @property
    def delta(self) -> _RealLike:
        return self.truemax-self.truemin

    def __post_init__(self):
        assert (self.min is not nan) and (self.max is not nan), "nan is not a Real number!"

        # should prevent empty ranges (n,n), (n,n], and [n,n)
        # [n,n] is the only valid case of equal min & max
        if not (self.excludes_min or self.excludes_max):
            assert (self.min <= self.max) and (self.max >= self.min), "min must be less than or equal to max with fully inclusive bounds"
        else:
            assert (self.min < self.max) and (self.max > self.min), "min must be less than max with any exclusive bounds"

        if (self.min is -inf):
            assert self.excludes_min, "a min of -inf must be exclusive"
        if (self.max is inf):
            assert self.excludes_max, "a max of inf must be exclusive"

    def __contains__(self, x: _RealLike) -> bool:
        return (self.truemin <= x <= self.truemax)

    def clamp(self, x: _RealLike) -> _RealLike:
        min, max = self.truemin, self.truemax
        if x < min:
            return min
        elif x > max:
            return max
        return x

    def scaleOf(self, x: _RealLike) -> _RealLike:
        min = self.truemin
        delta = self.truemax - min
        return (x-min) / delta


