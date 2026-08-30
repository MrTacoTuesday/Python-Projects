from math import comb, floor
import random
from typing import Hashable, List, TypeVar

_T = TypeVar("_T");
class SetList(List[_T], Hashable):
    def __hash__(self) -> int:
        return hash(self.__repr__());
    
    def __repr__(self) -> str:
        k = sorted(self).__repr__(); # type: ignore
        return "{" + k.removeprefix("[").removesuffix("]") + "}";
    
    def __eq__(self, other) -> bool:
        return sorted(self) == sorted(other); # type: ignore


def builder(l: list[int], n: int) -> list[list[int]]:
    result: list[list[int]] = [];
    for i in range(n - sum(l),-1,-1):
        result.append(l + [i]);
    return result;
        
def runner(c: int) -> list[list[int]]:
    N = 2*c - 1;
    result: list[list[int]] = builder([],N);
    _r: list[list[int]] = [];
    for _ in range(c-1):
        for set in result:
            _r.extend(builder(set,N));
        result = _r;
        _r = [];
    return result;


def votecomb(c: int, required_voting: bool = False) -> int:
    if required_voting:
        return comb(3*c - 2, c - 1);
    else:
        return comb(3*c - 1,c);
    
def g(c: int) -> int:
    return 2*comb(3*c,c)//(9*c-3);


#print(votecomb(14));

"""for x in range(1,28+1):
    a = comb(3*x-1,x);
    b = comb(3*x-2,x-1);
    c = a/b - 2;
    #print(f"x={x}: 2 + {a - 2*b}/{b} = 2 + {c}");
    print(f"x={x}: {(x-1)/x - c}");"""
    

def random_vote(c: int) -> list[int]:
    N = 2*c - 1;
    _r = [];
    for i in range(c):
        _r[i] = random.randint(0,N-(0 if i == 0 else _r[i-1]));
    return _r;

def random_votes(c: int, v: int) -> tuple[list[list[int]], list[int], list[int]]:
    N = 2*c - 1;
    votes = [];
    _v = [0 for _ in range(c)];
    _f = [0 for _ in range(c)];
    for _ in range(v):
        _r = [];
        for i in range(c):
            k = random.randint(0,N-(0 if i == 0 else _r[i-1]));
            _r[i] = k;
            _v[i] += k;
        M = max(_r);
        for i in range(c):
            _f[i] += floor(_r[i]/M);
        votes.append(_r);
        
    return (votes, _v, _f);


print(random_votes(3,1000));