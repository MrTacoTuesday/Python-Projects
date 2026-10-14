from collections.abc import Callable
import math


def mean(lst: list[float | int]) -> float | int:
    return math.fsum(lst) / len(lst)


__globals = {
    "ln": math.log,
    "log": math.log10,
    "logb": lambda x, b: math.log(x) / math.log(b),
    "e": math.e,
    "pi": math.pi,
    "exp": math.exp,
    "sqrt": math.sqrt,
    "root": lambda x, n: x ** (1 / n),
    "pow": math.pow,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "asinh": math.asinh,
    "acosh": math.acosh,
    "atanh": math.atanh,
    "floor": math.floor,
    "ceil": math.ceil,
    "gamma": math.gamma,
    "nCr": math.comb,
    "nPr": math.perm,
    "sign": math.copysign,
    "deg": math.degrees,
    "rad": math.radians,
    "product": math.prod,
    "sum": math.fsum,
    "tau": math.tau,
    "trunc": math.trunc,
    "mean": lambda lst: math.fsum(lst)/len(lst),
    "len": len,
    "abs": abs,
}

Num = float | int
Lst = list[Num]
Var = Num | Lst
def a_define(var: str, value: Var) -> Var:
    if isinstance(value, (Num, list)):
        __globals[var] = value
    else:
        raise TypeError(f"Invalid type for variable {var}")
    return __globals[var]


def func_x(raw: str)->Callable[[Var], Var]:
    def _(x: float | int) -> float | int:
        return eval(raw, __globals, {"x": x})
    return _

def func_xy(raw: str)->Callable[[Var, Var], Var]:
    def _(x: float | int) -> float | int:
        return eval(raw, __globals, {"x": x})
    return _

"""
sqrt(mean((x - ux)**2 for x in x))

"""