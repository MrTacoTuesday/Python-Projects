from collections.abc import Callable
from math import floor, log10


def superant(x: float, n: float = 1) -> float:
    return x**(x * n)


def superant_root(y: float, n: float = 1) -> float:
    _lcn = 1 / n * log10(y)
    _x0 = 3e0
    #print(f"\33[2;3m{y:.3f} @⁻¹ {n}\33[0m")
    #print(f"\33[2;3mExpexted x log x: {_lcn:.3f}\33[0m")
    for _ in range(1000):
        _t = _lcn - _x0 * log10(_x0)
        if abs(_t) <= 1e-16:
            return _x0
        dx = 10**(floor(log10(abs(_t))))
        if _t < 0:
            dx = -dx
        if _ < 100 and _ % 4 == 0:
            #print(f"\33[2;3m({_:03d}) Pred: {_x0 * log10(_x0):.6f}", end="")
            #print(f"\t\tResid: {_t:.6f} Guess: {_x0} Adj: {dx}\33[0m")
            pass
        _x0 += dx
    return _x0


def exultrant(x: float, n: float = 1) -> float:
    return x**(x**n)


def exultrant_root(y: float, n: float = 1) -> float:
    _l2c = log10(log10(y))
    _x0 = 3e0
    for _ in range(1000):
        _t = (_l2c - log10(log10(_x0))) / (log10(_x0)) - n
        if abs(_t) <= 1e-16:
            return _x0
        dx = 10**(floor(log10(abs(_t))))
        if _t < 0:
            dx = -dx
        # input(f"\33[2;3m{_t} {_x0} {dx}\33[0m") ## TESTING
        _x0 += dx
    return _x0


'''superant_eq_solve(x1,n1,x2,n2)
Solves an equation in the form of:
    x1^(x1*n1) = x2^(x2*n2)
for whichever input is left as None.
'''


def superant_eq_solve(x1: float | None = None,
                      n1: float | None = None,
                      x2: float | None = None,
                      n2: float | None = None) -> float:
    vars = (x1 is None) + (n1 is None) + (x2 is None) + (n2 is None)
    if vars == 0:
        raise ValueError("No unknown values.")
    if vars > 1:
        raise ValueError("Too many unknown values.")
    if x1 is None:
        if x2 is None or n2 is None or n1 is None:
            raise RuntimeError("Unreachable code")
        return superant_root(superant(x2, n2), n1)
    if x2 is None:
        if x1 is None or n2 is None or n1 is None:
            raise RuntimeError("Unreachable code")
        return superant_root(superant(x1, n1), n2)
    if n1 is None:
        if x2 is None or x1 is None or n2 is None:
            raise RuntimeError("Unreachable code")
        return log10(superant(x2, n2)) / (log10(x1) * x1)
    if n2 is None:
        if x2 is None or x1 is None or n1 is None:
            raise RuntimeError("Unreachable code")
        return log10(superant(x1, n1)) / (log10(x2) * x2)
    raise RuntimeError("Unreachable code")


'''exultrant_eq_solve(x1,n1,x2,n2)
Solves an equation in the form of:
    x1^(x1^n1) = x2^(x2^n2)
for whichever input is left as None.
'''


def exultrant_eq_solve(x1: float | None = None,
                       n1: float | None = None,
                       x2: float | None = None,
                       n2: float | None = None) -> float:
    vars = (x1 is None) + (n1 is None) + (x2 is None) + (n2 is None)
    if vars == 0:
        raise ValueError("No unknown values.")
    if vars > 1:
        raise ValueError("Too many unknown values.")
    if x1 is None:
        if x2 is None or n2 is None or n1 is None:
            raise RuntimeError("Unreachable code")
        return exultrant_root(exultrant(x2, n2), n1)
    if x2 is None:
        if x1 is None or n2 is None or n1 is None:
            raise RuntimeError("Unreachable code")
        return exultrant_root(exultrant(x1, n1), n2)
    if n1 is None:
        if x2 is None or x1 is None or n2 is None:
            raise RuntimeError("Unreachable code")
        return log10(log10(exultrant(x2, n2)) / log10(x1)) / log10(x1)
    if n2 is None:
        if x2 is None or x1 is None or n1 is None:
            raise RuntimeError("Unreachable code")
        return log10(log10(exultrant(x1, n1)) / log10(x2)) / log10(x2)
    raise RuntimeError("Unreachable code")


def test_eq(
    title: str, sym: str, x1: float, n1: float, n2: float,
    fx: Callable[[float, float], float], fy: Callable[[float, float], float],
    eqs: Callable[[float | None, float | None, float | None, float | None],
                  float]):
    print(f"\33[2;3m{title}\33[0m")
    print(f"Equation:\t{x1} {sym} {n1} == x {sym} {n2}")
    x2 = eqs(x1, n1, None, n2)
    print("x\t\t\t=", x2)
    y1, y2 = fx(x1, n1), fx(x2, n2)
    print(f"{x1:.2f} {sym} {n1:.2f} =", y1)
    print(f"{x2:.2f} {sym} {n2:.2f} =", y2)
    print()
    print(f"{y1:.2f} {sym}⁻¹ {n1:.2f} =", fy(y1, n1))
    print(f"{y2:.2f} {sym}⁻¹ {n2:.2f} =", fy(y2, n2))
    print()
    print()


test_eq("Superants (x @ n == x^(xn))", "@", 4, 1.05, 2, superant, superant_root,
        superant_eq_solve)
test_eq("Exultrants (x ¤ n == x^(x^n))", "¤", 2.8105, 1.8, 2, exultrant,
        exultrant_root, exultrant_eq_solve)

from sys import set_int_max_str_digits
#set_int_max_str_digits(100000)

print(exultrant(2, 28))