class Digit:

    def __init__(self, digit: "Digit | int" = 0):
        self.__value: int = digit if isinstance(digit, int) else digit.__value

    def next(self) -> "Digit":
        if self.__value == 9:
            self.__value = 0
        else:
            self.__value += 1
        return self

    def prev(self) -> "Digit":
        if self.__value == 0:
            self.__value = 9
        else:
            self.__value -= 1
        return self

    def __repr__(self):
        return f"{self.__value}"

    def __add__(self, other: "Digit") -> "tuple[Digit, bool]":
        q = self.__value + other.__value
        return (Digit(q % 10), q > 9)

    def __sub__(self, other: "Digit") -> "tuple[Digit, bool]":
        q = self.__value - other.__value
        return (Digit(q % 10), q < 0)

    def __mul__(self, other: "Digit") -> "tuple[Digit, Digit]":
        q = self.__value * other.__value
        return (Digit(q % 10), Digit(q // 10))

    def __gt__(self, other: "Digit") -> bool:
        return self.__value > other.__value

    def __eq__(self, other: "Digit") -> bool:
        return self.__value == other.__value
