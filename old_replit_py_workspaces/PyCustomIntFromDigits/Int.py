from typing import overload

from Digit import Digit


class Int:

    @staticmethod
    def zero() -> "Int":
        return Int([Digit()])

    def __init__(self, digits: list[Digit], sign: bool = False):
        self.__digits = digits
        self.__sign = sign

    def copy(self) -> "Int":
        return Int(self.__digits.copy(), self.__sign)

    def negated(self) -> "Int":
        return Int(self.__digits.copy(), not self.__sign)

    def negate(self):
        self.__sign = not self.__sign

    def abs(self) -> "Int":
        return Int(self.__digits.copy())

    @overload
    @staticmethod
    def parse(value: str) -> "Int":
        ...

    @overload
    @staticmethod
    def parse(value: int) -> "Int":
        ...

    @staticmethod
    def parse(value: str | int) -> "Int":
        if isinstance(value, str):
            sign = False
            if value[0] in "+-":
                sign = value[0] == "-"
            digits = []
            for s in value[sign:]:
                if not s.isdigit:
                    raise ValueError("Invalid string")
                digits.append(Digit(int(s)))
            if len(digits) == 0:
                raise ValueError("Invalid string")
            return Int(digits, sign)
        else:
            return Int.parse(str(value))

    @property
    def sign(self) -> "Int":
        if self.isZero:
            return Int.zero()
        return Int([Digit(1)], sign=self.__sign)

    @property
    def pyInt(self) -> int:
        return int(str(self))

    @property
    def digits(self) -> int:
        return len(self.__digits)

    @property
    def isZero(self) -> bool:
        self.__rem_left_zeroes()
        return self.__digits[0] == Digit()

    @property
    def isNegative(self) -> bool:
        return self.__sign

    def __repr__(self):
        s = "-" if self.__sign else ""
        return s + "".join(map(str, self.__digits))

    def __eq__(self, other: "Int") -> bool:
        if self.__sign != other.__sign:
            return False
        if len(self.__digits) != len(other.__digits):
            return False
        for i in range(len(self.__digits)):
            if not self.__digits[i] == other.__digits[i]:
                return False
        return True

    def __gt__(self, other: "Int") -> bool:
        if self.__sign != other.__sign:
            return other.__sign
        if len(self.__digits) > len(other.__digits):
            return True
        if len(self.__digits) == len(other.__digits):
            for i in range(len(self.__digits)):
                if self.__digits[i] > other.__digits[i]:
                    return True
                elif self.__digits[i] < other.__digits[i]:
                    return False
        return False

    def __ge__(self, other: "Int") -> bool:
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other: "Int") -> bool:
        return not self.__ge__(other)

    def __le__(self, other: "Int") -> bool:
        return not self.__gt__(other)

    def __add_digit(self, digit: Digit, pos: int):
        if pos >= 0:
            pass
        while abs(pos) > len(self.__digits):
            self.__digits.insert(0, Digit())
        d, c = self.__digits[pos] + digit
        self.__digits[pos] = d
        if c:
            self.__add_digit(Digit(1), pos - 1)

    def __add__(self, other: "Int") -> "Int":
        if self.__sign != other.__sign:
            return (self - other.negated())
        result = self.abs()
        i = -1
        while i >= -len(other.__digits):
            result.__add_digit(other.__digits[i], i)
            i -= 1
        result.__rem_left_zeroes()
        if self.__sign:
            result.negate()
        return result

    def __subt_digit(self, digit: Digit, pos: int):
        if pos >= 0:
            pass
        while abs(pos) > len(self.__digits):
            self.__digits.insert(0, Digit())
        d, c = self.__digits[pos] - digit
        self.__digits[pos] = d
        if c:
            self.__subt_digit(Digit(1), pos - 1)

    def __sub__(self, other: "Int") -> "Int":
        if self.__sign != other.__sign:
            return self + other.negated()
        a, b = self.abs(), other.abs()
        _ = self
        if a == b:
            return Int.zero()
        if a.__lt__(b):
            a, b = b, a
            _ = other
        result = a.copy()
        i = -1
        while i >= -len(b.__digits):
            result.__subt_digit(b.__digits[i], i)
            i -= 1
        result.__rem_left_zeroes()
        if _.__sign:
            result.negate()
        return result

    def __rem_left_zeroes(self):
        while self.__digits[0] == Digit():
            if len(self.__digits) == 1:
                self.__sign = False
                return
            self.__digits.pop(0)

    def _mult_digit(self, digit: Digit, pos: int) -> "Int":
        if pos >= 0:
            pass
        result = Int.zero()
        i = -1
        while i >= -len(self.__digits):
            a, b = self.__digits[i] * digit
            result.__add_digit(a, i + pos + 1)
            result.__add_digit(b, i + pos)
            i -= 1
        result.__rem_left_zeroes()
        return result

    def __mul__(self, other: "Int") -> "Int":
        result = Int.zero()
        i = -1
        while i >= -len(other.__digits):
            result += self._mult_digit(other.__digits[i], i)
            i -= 1
        if self.__sign != other.__sign:
            result.negate()
        return result

    def __div10(self):
        if len(self.__digits) == 1:
            self.__digits[0] = Digit()
        else:
            self.__digits.pop()

    def _start_div(self, other: "Int", digits: int, i: int = 0) -> Digit:
        while self.digits < digits:
            self.__digits.insert(0, Digit())
        a = Int(self.__digits[:i + 1])
        a.__rem_left_zeroes()
        if a < other:
            return Digit()
        _q = Digit(0)
        while other._mult_digit(_q, -1).__le__(a):
            _q.next()
        _q.prev()
        self.__digits = ((a - other._mult_digit(_q, -1)).__digits +
                         self.__digits[i + 1:])
        return _q

    def quorem(self, other: "Int") -> "tuple[Int, Int]":
        if other.isZero:
            raise ZeroDivisionError("division by zero")
        if self.isZero:
            return (Int.zero(), Int.zero())
        sign = self.__sign or other.__sign
        a, b = self.abs(), other.abs()
        if a < b:
            return (Int.zero(), self)
        if a == b:
            return (Int([Digit(1)], sign), Int.zero())
        _q = Int.zero()
        for i in range(self.digits):
            if a < b:
                break
            _q.__digits.append(a._start_div(b, self.digits, i))
        if sign:
            _q.negate()
        _q.__rem_left_zeroes()
        print()
        return (_q, a)

    def __floordiv__(self, other: "Int") -> "Int":
        return self.quorem(other)[0]

    def __mod__(self, other: "Int") -> "Int":
        return self.quorem(other)[1]

    def __truediv__(self, other: "Int") -> "Int":
        return self.__floordiv__(other)

    def __format__(self, format_spec: str) -> str:
        #print("fs=", format_spec)
        if format_spec == "":
            return str(self)
        if format_spec[-1] == "d":
            i = 0
            if len(format_spec) > 1:
                i = int(format_spec[:-1])
            #print(i)
            s = str(self.abs())
            _ = "0" if format_spec[0] == "0" else " "
            s = ("-" if self.__sign else "+") + (_ * (i - len(s))) + s
            self.__rem_left_zeroes()
            return s
        return str(self)
