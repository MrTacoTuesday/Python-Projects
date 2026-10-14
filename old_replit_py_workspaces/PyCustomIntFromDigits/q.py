from typing import Literal


def int_division(a: int, b: int) -> tuple[int, int]:
    if a == 0:
        return (0, 0)
    if a == b:
        return (1, 0)
    _q, _r = 0, 0
    while _q * b <= a - b:
        _q += 1
    _r = a - _q * b
    return (_q, _r)


d = int_division


def division(a: float, b: float, __n: int = 0) -> float:
    if __n >= 18:
        return 0
    if a == 0:
        return 0.0
    if a == b:
        return 1.0
    _q, _r = 0, 0
    while _q * b <= a - b:
        _q += 1
    _r = a - _q * b
    #print(f"{_q} {_r}")
    return _q + division(_r * 10, b, __n + 1) / 10


print(division(128, 7))
print(128 / 7)


def mult(a: int, b: int, __n: int = 0) -> int:
    if __n >= b:
        return 0
    if a == 0 or b == 0:
        return 0
    return a + mult(a, b, __n + 1)
