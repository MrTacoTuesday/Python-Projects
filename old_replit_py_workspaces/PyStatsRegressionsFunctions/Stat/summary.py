class Summary:

    def __init__(self, data: dict[float, float]):
        self.__n = sum(data.values())
        self.__sumX = sum(x * f for x, f in data.items())
        self.__sumX2 = sum(x**2 * f for x, f in data.items())
        self.__meanX = self.__sumX / self.__n
        self.__varianceX = sum(
            (x - self.__meanX)**2 * f for x, f in data.items())
        self.__sampDevX = (self.__varianceX / (self.__n - 1))**0.5
        self.__popDevX = (self.__varianceX / self.__n)**0.5

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

    def __repr__(self):
        return ("Summary:" + f"\n\tn: {str(self.__n)}" +
                f"\n\tΣx = {str(self.__sumX)}" +
                f"\n\tΣx² = {str(self.__sumX2)}" +
                f"\n\tx̅ = {str(self.__meanX)}" +
                f"\n\tΣ(x-x̅)² = {str(self.__varianceX)}" +
                f"\n\tsx = {str(self.__sampDevX)}" +
                f"\n\tσx = {str(self.__popDevX)}" + "\n")
