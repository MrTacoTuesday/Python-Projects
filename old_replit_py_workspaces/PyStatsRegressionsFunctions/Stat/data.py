from collections.abc import Callable
from typing import Literal

from Stat.summary import Summary
from Stat.summary2 import Summary2


class Data:

    @staticmethod
    def fromData(data: "Data") -> "Data":
        return Data(data.data, title=data.title, type=data.summaryType)

    def __init__(self,
                 lst: list[float] | dict[float, float],
                 frq: list[float] | None = None,
                 type: Literal["OneVar", "TwoVar"] | None = "OneVar",
                 title: str = "Data"):
        if isinstance(lst, dict):
            if frq:
                raise ValueError("frq must be None if lst is a dict")
            self.__data = lst
        elif frq and len(frq) != len(lst):
            raise ValueError("frq and lst must have the same length")
        else:
            self.__data = dict(zip(lst, frq or [1] * len(lst), strict=True))
        self.title = title
        self.summaryType: Literal["OneVar", "TwoVar"] | None = type

    def __repr__(self):
        return (f"{self.title}:\n\t" +
                "\n\t".join([f"{x}: {y}" for x, y in self.__data.items()]) +
                "\n" + self.__get_summary__())

    def __get_summary__(self) -> str:
        if self.summaryType == "OneVar":
            return str(self.OneVar)
        elif self.summaryType == "TwoVar":
            return str(self.TwoVar)
        return ""

    def splitXY(self) -> "tuple[Data, Data]":
        return (Data(self.xList), Data(self.yList))

    @property
    def xList(self) -> list[float]:
        return list(self.__data.keys())

    @property
    def yList(self) -> list[float]:
        return list(self.__data.values())

    @property
    def data(self) -> dict[float, float]:
        return self.__data

    @property
    def OneVar(self) -> Summary:
        return Summary(self.__data)

    @property
    def TwoVar(self) -> Summary2:
        return Summary2(self.xList, self.yList)

    def shifted(self, by: float) -> "Data":
        return Data({x + by: y
                     for x, y in self.__data.items()},
                    title=self.title,
                    type=self.summaryType)

    def scaled(self, by: float) -> "Data":
        return Data({x: y * by
                     for x, y in self.__data.items()},
                    title=self.title,
                    type=self.summaryType)

    def modifiedX(self, using: Callable[[float], float]) -> "Data":
        return Data({using(x): y
                     for x, y in self.__data.items()},
                    title=self.title,
                    type=self.summaryType)

    def modifiedY(self, using: Callable[[float], float]) -> "Data":
        return Data({x: using(y)
                     for x, y in self.__data.items()},
                    title=self.title,
                    type=self.summaryType)

    def modified(self, fx: Callable[[float], float],
                 fy: Callable[[float], float]) -> "Data":
        return Data({fx(x): fy(y)
                     for x, y in self.__data.items()},
                    title=self.title,
                    type=self.summaryType)

    def cumulated(self) -> "Data":
        _f, t = 0, sum(self.yList)
        fl = []
        for f in self.yList:
            _f += f
            fl.append(_f / t)
        return Data(self.xList, fl)
