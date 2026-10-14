from collections.abc import Callable
from typing import Literal

from utility import FreqTable, NumList, freq_dict

from .Summary1V import Summary1V
from .Summary2V import Summary2V


class Data:

    @staticmethod
    def fromData(data: "Data") -> "Data":
        return Data(data.data, title=data.title, type=data.summaryType)

    def __init__(self,
                 lst: NumList | FreqTable,
                 frq: NumList | None = None,
                 type: Literal["OneVar", "TwoVar"] | None = "OneVar",
                 title: str = "Data"):
        if isinstance(lst, dict):
            if frq:
                raise ValueError("frq must be None if lst is a dict")
            self.__data = lst
        elif frq is not None and len(frq) != len(lst):
            raise ValueError("frq and lst must have the same length")
        else:
            if frq is None:
                self.__data = freq_dict(lst)
            else:
                self.__data = dict(zip(lst, frq, strict=True))
        self.title = title
        self.summaryType: Literal["OneVar", "TwoVar"] | None = type

    def __repr__(self):
        return (f"{self.title}:\n\t" + "\n\t".join(
            [f"{x}: {y}" for x, y in sorted(self.__data.items())]) + "\n" +
                self.__get_summary__())

    def __get_summary__(self) -> str:
        if self.summaryType == "OneVar":
            return str(self.OneVar)
        elif self.summaryType == "TwoVar":
            return str(self.TwoVar)
        return ""

    def splitXY(self) -> "tuple[Data, Data]":
        return (Data(self.xList), Data(self.yList))

    @property
    def xList(self) -> NumList:
        return list(self.__data.keys())

    @property
    def yList(self) -> NumList:
        return list(self.__data.values())

    @property
    def data(self) -> FreqTable:
        return self.__data

    @property
    def OneVar(self) -> Summary1V:
        return Summary1V(self.__data)

    @property
    def TwoVar(self) -> Summary2V:
        return Summary2V(self.xList, self.yList)

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

    def toList(self) -> NumList:
        _q: NumList = []
        for x, y in self.__data.items():
            if not isinstance(y, int) and int(y) != y:
                raise ValueError("Frequencies must be integers")
            _q.extend([x] * int(y))
        return _q
