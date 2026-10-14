###### UTILS.PY ######
## Helper functions for my programs ##

from typing import Callable, List, TypeVar

_T = TypeVar("_T")


def cstr(color: int, *values: object, clr: bool = True) -> str:
    c = f"\33[{color}m"
    s = ""
    for i in range(len(values)):
        if i > 0:
            s += " "
        s += c + str(values[i]) + ("\33[0m" if clr else "")
    return s


def fstr(ansi: List[int] | int, *values: object, clr: bool = True) -> str:
    _f = ""
    ansi = [ansi] if isinstance(ansi, int) else ansi
    for i in ansi:
        _f += f"{i};"
    _f = f"\33[{_f[0: -1]}m"
    s = ""
    CLR = "\33[0m" if clr else ""
    for i in range(len(values)):
        if i > 0:
            s += " "
        s += f"{_f}{values[i]}{CLR}"
    return s


def cprint(color: int, *values: object):
    print(cstr(color, *values))


def fprint(ansi: List[int] | int, *values: object):
    print(fstr(ansi, *values))


def get_info_as(
        prompt: str,
        valid_in: Callable[[str], bool] = lambda _: True,
        format: Callable[[str], _T] = lambda x: x,
        err_msg: Callable[[str], str] | str = "Invalid response") -> _T:
    err: Callable[[str],
                  str] = (lambda x: x) if isinstance(err_msg, str) else err_msg
    valid = False
    while not valid:
        _res = input(prompt)
        try:
            valid = valid_in(_res)
        except Exception:
            valid = False
            print(err(_res))
    return format(_res)
