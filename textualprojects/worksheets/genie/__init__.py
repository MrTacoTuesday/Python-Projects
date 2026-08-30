from math import isnan, isinf
if __name__ == "__main__":
    from sieve_of_eratosthenes import find_primes, factorize, common_factors;
else:
    from .sieve_of_eratosthenes import find_primes, factorize, common_factors;

def reduce_fractional_ratio(n: int, d: int) -> tuple[int, int]:
    if n == 0 and d==0:
        return 0,0;
    elif n == 0:
        return 0,1;
    elif d == 0:
        return 1,0;
    
    s: int = -1 if n*d < 0 else 1;
    n,d = abs(n),abs(d);
    
    p: int = 2;
    while n!=1 and d!=1 and p <= min(n,d):
        while n%p==0 and d%p==0:
            n,d = n//p, d//p;
        p+=1;
        
    return s*n,d;

def approx_to_fractional_ratio(f: float, epsilon: float = 1e-8, /) -> tuple[int, int]: 
    if f == 0:
        return 0,1;
    elif isnan(f):
        return 0,0;
    elif isinf(f):
        return 1,0;
    elif f.is_integer():
        return int(f),1;
    
    n,d = 0,1;
    s = -1 if f < 0 else 1;
    
    f,c  = abs(f), abs(f);
    while True:
        n += d * int(c);
        c -= int(c);
        if abs(n/d - f) <= epsilon:
            break;
        n,d = reduce_fractional_ratio(d,n);
        c = 1/c;
    return reduce_fractional_ratio(s*n,d);

__all__ = [
    "find_primes", "factorize", "common_factors", "reduce_fractional_ratio", "approx_to_fractional_ratio"
]