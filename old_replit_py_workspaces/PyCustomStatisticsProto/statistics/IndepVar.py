from collections.abc import Callable
from random import choices
from typing import Literal, final

from .Data import Data


@final
class IndepVar(Data):

    @staticmethod
    def fromData(data: Data) -> "IndepVar":
        return IndepVar(data.data, type=data.summaryType, title=data.title)

    def __init__(self,
                 lst: list[float] | dict[float, float],
                 frq: list[float] | None = None,
                 type: Literal["OneVar"] | Literal["TwoVar"] | None = "OneVar",
                 title: str = "Independant Variable"):
        super().__init__(lst, frq, type, title)

    def repeated(self, n: int) -> "IndepVar":
        iv = IndepVar(self.data)
        if n < 1:
            raise ValueError("n must be greater than 0")
        for _ in range(n):
            if _ == 0:
                continue
            iv = iv + self
        return iv

    def pow(self, n: int) -> "IndepVar":
        iv = IndepVar(self.data)
        if n < 1:
            raise ValueError("n must be greater than 0")
        for _ in range(n):
            if _ == 0:
                continue
            iv = iv * self
        return iv

    def truncatedX(self) -> "IndepVar":
        d: dict[float, float] = {}
        for x, y in self.data.items():
            d[round(x)] = d.get(round(x), 0) + y
        return IndepVar(d)

    #@override
    def shifted(self, by: float) -> "IndepVar":
        return IndepVar.fromData(super().shifted(by))

    #@override
    def scaled(self, by: float) -> "IndepVar":
        return IndepVar.fromData(super().scaled(by))

    #@override
    def modifiedX(self, using: Callable[[float], float]) -> "IndepVar":
        return IndepVar.fromData(super().modifiedX(using))

    #@override
    def modifiedY(self, using: Callable[[float], float]) -> "IndepVar":
        return IndepVar.fromData(super().modifiedY(using))

    #@override
    def modified(self, fx: Callable[[float], float],
                 fy: Callable[[float], float]) -> "IndepVar":
        return IndepVar.fromData(super().modified(fx, fy))

    def __map(self, other: "IndepVar", fx: Callable[[float, float],
                                                    float]) -> "IndepVar":
        q = {}
        for xa, pa in self.data.items():
            for xb, pb in other.data.items():
                x = fx(xa, xb)
                q[x] = q.get(x, 0) + pa * pb
        return IndepVar(q)

    def __add__(self, other: "IndepVar") -> "IndepVar":
        return self.__map(other, lambda x, y: x + y)

    def __sub__(self, other: "IndepVar") -> "IndepVar":
        return self.__map(other, lambda x, y: x - y)

    def __mul__(self, other: "IndepVar") -> "IndepVar":
        return self.__map(other, lambda x, y: x * y)

    def __truediv__(self, other: "IndepVar") -> "IndepVar":
        return self.__map(other, lambda x, y: x / y)

    def random(self, count: int = 1) -> list[float]:
        return choices(list(self.data.keys()),
                       list(self.data.values()),
                       k=count)
