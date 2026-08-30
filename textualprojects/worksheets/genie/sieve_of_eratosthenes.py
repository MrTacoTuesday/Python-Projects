
## TODO: Test new version that uses lists instead of sets... might be even faster and accurate
def find_primes(to: int, /) -> set[int]:
    assert to > 1;
    primes = set[int]();
    numbers = {i for i in range(2,to+1)};
    while len(numbers) != 0:
        p: int = numbers.pop();
        primes.add(p);
        numbers.difference_update({j*p for j in range(2,to//p+1)});
    return primes;

def factorize(n: int, /) -> list[int]:
    if n == 0: return [0];
    elif abs(n) == 1: return [n];
    f = [-1 if n < 0 else 1];
    n = abs(n);
    p: int = 2;
    while n != 1:
        while n%p == 0:
            n//=p;
            f.append(p);
        p+=1;
    return f;

def is_prime(n: int, /) -> bool:
    if n == 0: return False;
    elif n == 1: return True;
    elif n < 0: return False;
    p: int = 2;
    while n != 1:
        if n%p == 0:
            return n==p
        p+=1;
    raise SystemError()

def common_factors(*nums: int) -> list[int]:
    if len(nums) == 0: 
        return [];
    elif len(nums) == 1:
        return factorize(nums[0]);
    if 0 in nums: return [0] if set(nums)=={0} else [];
    
    f: list[int] = [-1 if all((n<0 for n in nums)) else 1];
    n: tuple[int, ...] = tuple((abs(n) for n in nums));
    p: int = 2;
    while all((n != 1 for n in n)) and p < min(n):
        while all((n%p==0 for n in n)):
            n = tuple((n//p for n in n));
            f.append(p);
        p+=1;
    return f;

"""
# old version, new incorporates prime algorithm directly, over 2x faster
def __factorize(n: int) -> list[int]:
    if n == 0: return [0];
    elif abs(n) == 1: return [n];
    f = [-1 if n < 0 else 1];
    n = abs(n);
    for prime in find_primes(n):
        while n%prime == 0:
            n//=prime;
            f.append(prime);
    return f;
    """

"""
# old version, newest has much faster runtime, like 100x faster *sob*
def _factorize(n: int) -> list[int]:
    if n == 0: return [0];
    elif abs(n) == 1: return [n];
    f = [-1 if n < 0 else 1];
    n = abs(n);
    numbers = {i for i in range(2,n+1)};
    while n != 1:
        p: int = numbers.pop();
        while n%p == 0:
            n//=p;
            f.append(p);
        numbers.difference_update({j*p for j in range(2,n//p+1)});
    return f;
    """

if __name__ == "__main__":
    """from random import randint;
    import timeit;
    
    arg = [randint(100,1000000)for _ in range(2)];
    exe = "common_factors(*arg)";
    
    print("Execution Arguments:", *arg);
    print("Execution Time:", timeit.timeit(f"print('Execution Result:', {exe});", number=1, globals=globals()));
    """
    args = (
        1413,
        1368,
        17_652
    )
    for arg in args:
        factors = factorize(arg)
        print(factors)
        assert all(is_prime(n) for n in factors)
    print(common_factors(1368, 17_652))