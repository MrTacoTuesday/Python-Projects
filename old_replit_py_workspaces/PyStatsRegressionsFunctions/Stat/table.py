from collections.abc import Callable
from typing import Literal

from Stat.data import Data


class Table(Data):

    @staticmethod
    def fromData(data: Data) -> "Table":
        _t = None if data.summaryType == "OneVar" else data.summaryType
        return Table(data.data, title=data.title, type=_t)

    @staticmethod
    def fill(xValues: list[float] | int,
             fx: Callable[[float], float],
             type: Literal["TwoVar"] | None = "TwoVar",
             title: str = "Data Table"):
        x = xValues if isinstance(
            xValues, list) else [float(i) for i in range(xValues)]
        y = [fx(i) for i in x]
        return Table(x, y, type, title)

    def __init__(self,
                 x: list[float] | dict[float, float],
                 y: list[float] | None = None,
                 type: Literal["TwoVar"] | None = "TwoVar",
                 title: str = "Data Table"):
        super().__init__(x, y, type, title)

    def shifted(self, by: float) -> "Table":
        return Table.fromData(super().shifted(by))

    def scaled(self, by: float) -> "Table":
        return Table.fromData(super().scaled(by))

    def modifiedX(self, using: Callable[[float], float]) -> "Table":
        return Table.fromData(super().modifiedX(using))

    def modifiedY(self, using: Callable[[float], float]) -> "Table":
        return Table.fromData(super().modifiedY(using))

    def modified(self, fx: Callable[[float], float],
                 fy: Callable[[float], float]) -> "Table":
        return Table.fromData(super().modified(fx, fy))


#5374685
