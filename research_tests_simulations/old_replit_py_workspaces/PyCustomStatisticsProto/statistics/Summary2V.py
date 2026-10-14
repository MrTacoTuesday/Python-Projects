from typing import final

from .Summary import Summary


@final
class Summary2V(Summary):

    def __init__(self,
                 x: list[float],
                 y: list[float],
                 title: str = "Two Var Summary"):
        if len(x) != len(y):
            raise ValueError("x and y must have the same number of elements")

        self.title = title

        self.__n = len(x)

        self.__sumX = sum(x)
        self.__sumX2 = sum(x**2 for x in x)
        self.__meanX = self.__sumX / self.__n
        self.__varianceX = sum((x - self.__meanX)**2 for x in x)
        self.__sampDevX = (self.__varianceX / (self.__n - 1))**0.5
        self.__popDevX = (self.__varianceX / (self.__n))**0.5

        self.__sumY = sum(y)
        self.__sumY2 = sum(y**2 for y in y)
        self.__meanY = self.__sumY / self.__n
        self.__varianceY = sum((y - self.__meanY)**2 for y in y)
        self.__sampDevY = (self.__varianceY / (self.__n - 1))**0.5
        self.__popDevY = (self.__varianceY / (self.__n))**0.5

        self.__sumXY = sum(x * y for x, y in zip(x, y, strict=True))

        self.__r = ((1 / (self.__n - 1)) * sum(
            (x - self.__meanX) / self.__sampDevX *
            (y - self.__meanY) / self.__sampDevY
            for x, y in zip(x, y, strict=True)))

        self.__b = (self.__r * self.__sampDevY / self.__sampDevX)
        self.__a = (self.__meanY - self.__b * self.__meanX)

    @property
    def n(self) -> float:
        return self.__n

    @property
    def sumX(self) -> float:
        return self.__sumX

    @property
    def sumX2(self) -> float:
        return self.__sumX2

    @property
    def meanX(self) -> float:
        return self.__meanX

    @property
    def varianceX(self) -> float:
        return self.__varianceX

    @property
    def sampDevX(self) -> float:
        return self.__sampDevX

    @property
    def popDevX(self) -> float:
        return self.__popDevX

    @property
    def sumY(self) -> float:
        return self.__sumY

    @property
    def sumY2(self) -> float:
        return self.__sumY

    @property
    def meanY(self) -> float:
        return self.__meanY

    @property
    def varianceY(self) -> float:
        return self.__varianceY

    @property
    def sampDevY(self) -> float:
        return self.__sampDevY

    @property
    def popDevY(self) -> float:
        return self.__popDevY

    @property
    def sumXY(self) -> float:
        return self.__sumXY

    @property
    def a(self) -> float:
        return self.__a

    @property
    def b(self) -> float:
        return self.__b

    @property
    def r(self) -> float:
        return self.__r

    def __repr__(self):
        return (f"{self.title}:" + f"\n\tn = {self.n}" +
                f"\n\tΣx = {self.sumX}" + f"\n\tΣy = {self.sumY}" +
                f"\n\tΣx² = {self.sumX2}" + f"\n\tΣy² = {self.sumY2}" +
                f"\n\tΣxy = {self.sumXY}" + f"\n\tx̅ = {self.meanX}" +
                f"\n\ty̅ = {self.meanY}" + f"\n\tsx = {self.sampDevX}" +
                f"\n\tsy = {self.sampDevY}" + "\n")
