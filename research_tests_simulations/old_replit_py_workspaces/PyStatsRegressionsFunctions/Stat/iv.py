from collections.abc import Callable
from random import choices
from typing import Literal

from .data import Data


class IV(Data):

    @staticmethod
    def fromData(data: Data) -> "IV":
        return IV(data.data, type=data.summaryType, title=data.title)

    def __init__(self,
                 lst: list[float] | dict[float, float],
                 frq: list[float] | None = None,
                 type: Literal["OneVar"] | Literal["TwoVar"] | None = "OneVar",
                 title: str = "Data"):
        super().__init__(lst, frq, type, title)
        self.title = "Independant Variable"

    def repeated(self, n: int) -> "IV":
        iv = IV(self.data)
        if n < 1:
            raise ValueError("n must be greater than 0")
        for _ in range(n):
            if _ == 0:
                continue
            iv = iv + self
        return iv

    def truncatedX(self) -> "IV":
        d: dict[float, float] = {}
        for x, y in self.data.items():
            d[round(x)] = d.get(round(x), 0) + y
        return IV(d)

    #@override
    def shifted(self, by: float) -> "IV":
        return IV.fromData(super().shifted(by))

    #@override
    def scaled(self, by: float) -> "IV":
        return IV.fromData(super().scaled(by))

    #@override
    def modifiedX(self, using: Callable[[float], float]) -> "IV":
        return IV.fromData(super().modifiedX(using))

    #@override
    def modifiedY(self, using: Callable[[float], float]) -> "IV":
        return IV.fromData(super().modifiedY(using))

    #@override
    def modified(self, fx: Callable[[float], float],
                 fy: Callable[[float], float]) -> "IV":
        return IV.fromData(super().modified(fx, fy))

    def __map(self, other: "IV", fx: Callable[[float, float], float]) -> "IV":
        q = {}
        for xa, pa in self.data.items():
            for xb, pb in other.data.items():
                x = fx(xa, xb)
                q[x] = q.get(x, 0) + pa * pb
        return IV(q)

    def __add__(self, other: "IV") -> "IV":
        return self.__map(other, lambda x, y: x + y)

    def __sub__(self, other: "IV") -> "IV":
        return self.__map(other, lambda x, y: x - y)

    def __mul__(self, other: "IV") -> "IV":
        return self.__map(other, lambda x, y: x * y)

    def __truediv__(self, other: "IV") -> "IV":
        return self.__map(other, lambda x, y: x / y)

    def random(self, count: int = 1) -> list[float]:
        return choices(list(self.data.keys()),
                       list(self.data.values()),
                       k=count)
