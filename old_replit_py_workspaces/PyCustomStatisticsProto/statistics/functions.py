from typing import overload

from utility import Number, NumList


@overload
def mean(lst: NumList) -> Number:
    ...


@overload
def mean(*lst: Number) -> Number:
    ...


def mean(lst: NumList | Number, *A: Number) -> Number:
    if isinstance(lst, list):
        _l = [*lst, *A]
        return sum(_l) / len(_l)
    else:
        return (lst + sum(A)) / (1 + len(A))


def variance(lst: NumList) -> Number:
    Mean = mean(lst)
    return sum((x - Mean)**2 for x in lst)


def sampleDeviation(lst: NumList) -> Number:
    return (variance(lst) / (len(lst) - 1))**0.5


def populationDeviation(lst: NumList) -> Number:
    return (variance(lst) / len(lst))**0.5


def size(lst: NumList) -> Number:
    return len(lst)


def sumA(A: NumList) -> Number:
    return sum(A)


def sumA2(A: NumList) -> Number:
    return sum(x**2 for x in A)


def correlation(A: NumList, B: NumList) -> Number:
    n, meanA, meanB = len(A), mean(A), mean(B)
    sdA, sdB = sampleDeviation(A), sampleDeviation(B)
    return ((1 / (n - 1)) * sum((x - meanA) / sdA * (y - meanB) / sdB
                                for x, y in zip(A, B, strict=True)))


def sumAB(A: NumList, B: NumList) -> Number:
    return sum(x * y for x, y in zip(A, B, strict=True))


def sumA2B(A: NumList, B: NumList) -> Number:
    return sum(x**2 * y for x, y in zip(A, B, strict=True))


def sumAB2(A: NumList, B: NumList) -> Number:
    return sumA2B(B, A)


def sumA2B2(A: NumList, B: NumList) -> Number:
    return sum((x * y)**2 for x, y in zip(A, B, strict=True))
