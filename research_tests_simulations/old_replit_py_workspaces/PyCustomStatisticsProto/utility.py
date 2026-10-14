from typing import Callable, Dict, List, TypeAlias

Number: TypeAlias = float | int
NumList: TypeAlias = List[Number]
Samples: TypeAlias = List[NumList]
FreqTable: TypeAlias = Dict[Number, Number]
StatFunc: TypeAlias = Callable[[NumList], Number]


def freq_dict(list: List[Number], rounding: int | None = None) -> FreqTable:
    _d: FreqTable = {}
    for item in sorted(list):
        _k = item if rounding is None else round(item, rounding)
        _d.setdefault(_k, 0)
        _d[_k] += 1
    return _d


def fancy_print_dict(dict: FreqTable, title: str | None = None) -> FreqTable:
    if title:
        print(title)
    for k in sorted(dict.keys()):
        print(("\t" if title else "") + f"{k:>3.3f} : {dict[k]:>6d}")
    return dict


def fancy_print_list(list: List[Number],
                     rounding: int = 3,
                     title: str | None = None) -> FreqTable:
    return fancy_print_dict(freq_dict(list, rounding), title)
