from typing import Any, Literal, TypeAlias, cast

UINT_64_MAX = 0xFFFF_FFFF_FFFF_FFFF
UINT_64_INT_OFFSET = 0x8000_0000_0000_0000
SALT = (
    0x301226781111FAEE,
    0xDECE101852E33B31,
    0x6459F065E91B8408,
    0x62C7698F19AD5C27,
    0x474EBAFAE938C63E,
    0xC4B1826AD1D42696,
    0x7909BB6B4260ED07,
    0x274AC0AED25DCB73,
    0x83AEC6080C63B230,
    0x5AFDDDC100001D63,
    0x901E6B6A65A5F832,
    0xB78878ADDDA0A3F5,
    0xEA48AC48EAA2488,
    0x3091FFA56E139233,
    0x9B361E270A2607EB,
    0xE9B710875FE1CEE,
)

HasherMode: TypeAlias = Literal['reset', 'preserve', 'merge']
class Hasher:

    def __init__(self, seed: int = 0, mode: HasherMode = 'merge') -> None:
        self.seed = seed
        self._digest = self.seed
        self._k = 0
        self._mode = mode
        
    @property
    def pre_digest(self) -> int:
        return self._digest

    @property
    def mode(self) -> HasherMode:
        return cast(HasherMode, self._mode)
    
    def deepcopy(self) -> Hasher:
        h = Hasher(self.seed)
        h._digest = self._digest
        h._k = self._k
        h._mode = self._mode
        return h
    
    def copy(self) -> Hasher:
        return self.deepcopy()

    def _prepare(self, o: Any) -> int:
        if isinstance(o, int):
            return o
        elif isinstance(o, float):
            return int(float.hex(o), base=16)
        elif isinstance(o, str):
            return int(o.encode().hex(), base=16)
        elif isinstance(o, bytes):
            return int(o.hex(), base=16)
        elif slots := cast(tuple[str], getattr(o, "__slots__")):
            q = 0
            for i in range(len(slots)):
                q ^= self._prepare(getattr(o, slots[i])) * SALT[(2 * i) % 16]
                q *= SALT[(2 * i + 1) % 16]
                q &= UINT_64_MAX
            return q
        return 0  # NotImplemented, but still accepted

    def _salt(self, i: int) -> int:
        return SALT[(i + self._k) & 0xF]

    def combine(self, *args: Any) -> Hasher:
        h = self._digest
        for o in args:
            o = self._prepare(o)

            h ^= (o * self._salt(8)) ^ ((o >> 32) * (h >> 32)) ^ self._salt(11) ^ self._salt(3)
            h ^= (h >> 48) * self._salt(0)
            h *= self._salt(1)
            h &= UINT_64_MAX
            h ^= ((h >> 32) * self._salt(2)) ^ ((h >> 34) * self._salt(3))
            h *= self._salt(4)
            h &= UINT_64_MAX

            self._k += 1
        self._digest = h
        return self

    def digest(self) -> HashDigest:
        h = self._digest

        h ^= (
            ((h >> 16) * self._salt(5))
            ^ ((h >> 20) * self._salt(6))
            ^ ((h >> 8) * self._salt(7))
        )
        h ^= ((h >> 34) * self._salt(1)) ^ ((h >> 36) * self._salt(4))
        h *= self._salt(8)
        h &= UINT_64_MAX
        h ^= (
            ((h >> 8) * self._salt(9))
            ^ ((h >> 16) * self._salt(10))
            ^ ((h >> 2) * self._salt(11))
            ^ ((h >> 9) * self._salt(12))
        )
        h ^= (
            ((h >> 18) * self._salt(1))
            ^ ((h >> 22) * self._salt(6))
            ^ ((h >> 10) * self._salt(9))
        )
        h *= self._salt(7)
        h &= UINT_64_MAX
        h ^= (
            ((h >> 4) * self._salt(13))
            ^ ((h >> 20) * self._salt(14))
            ^ ((h >> 1) * self._salt(15))
        )
        h ^= ((h >> 38) * self._salt(5)) ^ ((h >> 40) * self._salt(13))
        h ^= self.seed
        h &= UINT_64_MAX

        match self._mode:
            case 'merge':
                self.seed = h
                self._digest = h
                self._k = 0
            case 'reset':
                self._digest = self.seed
                self._k = 0
            case 'preserve' | _:
                pass
        
        return HashDigest(_value=h)
    
    def nextstate(self) -> Hasher:
        self.digest()
        return self

    def __int__(self) -> int:
        return int(self.deepcopy().digest())
    
    def __float__(self) -> float: # range of [0,1]
        return float(self.deepcopy().digest())
    
    def __str__(self) -> str:
        return str(self.deepcopy().digest())

class HashDigest:

    def __init__(self, *, _value: int) -> None:
        self._value = _value

    def __int__(self) -> int:
        return self._value

    def __index__(self) -> int:
        return self._value

    def __float__(self) -> float:
        return (self._value & UINT_64_MAX) / UINT_64_MAX

    def __str__(self) -> str:
        return hex(self._value)
