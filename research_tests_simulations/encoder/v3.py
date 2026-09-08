from abc import abstractmethod
from collections.abc import Buffer, Iterable
from ctypes import c_buffer, c_byte, c_double, c_float, c_int16, c_int64, c_int8, c_ubyte, c_uint16, c_uint8
import ctypes
from io import BytesIO
from typing import Any, Callable, ClassVar, Protocol, Self

CONST_UINT64_MAX = 0xFFFF_FFFF_FFFF_FFFF

class SupportsWrite[T](Protocol):

    @abstractmethod
    def write(self, o: T) -> None: 
        raise NotImplementedError



## I give up on reinventing the wheel...  for now.
import pickle
def encode_into(obj: Any, file: SupportsWrite[bytes]) -> None:
    return pickle.dump(obj, file, protocol=5)
def encode(obj: Any) -> bytes:
    return pickle.dumps(obj, protocol=5)


_SALT = (
    0x301226781111FAEE, 0xDECE101852E33B31, 0x6459F065E91B8408, 0x62C7698F19AD5C27,
    0x474EBAFAE938C63E, 0xC4B1826AD1D42696, 0x7909BB6B4260ED07, 0x274AC0AED25DCB73,
    0x83AEC6080C63B230, 0x5AFDDDC100001D63, 0x901E6B6A65A5F832, 0xB78878ADDDA0A3F5,
    0x0EA48AC48EAA2488, 0x3091FFA56E139233, 0x9B361E270A2607EB, 0x0E9B710875FE1CEE,
    0x8a5a2938e5c41938, 0xec469fcb2fbf2d57, 0x49e2c4047e3cd8e6, 0x81f94f2b1753dbc3, 
    0x42b804233456956a, 0x25a68ded8c00cd53, 0x83dd22bc414f5a64, 0xd24e92867640aeba, 
    0x1180f7a66964beed, 0x4b84eb07a3e4896c, 0x752dba7812998caa, 0x161b4b24f31e3fe6, 
    0xba425ed1c85a44d8, 0x3ee633f35f7d40dc, 0xf18d10f0fdaeed0e, 0x4a244d63308ebc91,
)
_SALT_LEN = len(_SALT)
def salt(i: int) -> int:
    return _SALT[i%_SALT_LEN]

class Hasher:
    PythonObjectEncoder: ClassVar[Callable[[Any], Buffer]] = encode

    @classmethod
    def from_time(cls) -> Self:
        from time import time_ns
        return cls(seed=memoryview(c_int64(time_ns())))

    def __init__(self, seed: Buffer | Any = b'') -> None:
        if isinstance(seed, Buffer):
            self.seed(seed)
        else:
            self.seed_any(seed)

    def seed(self, seed: Buffer) -> None:
        self._value = 0
        self._position = 0
        self.combine(seed)
        self._seed = self._value
        self._position = 0

    def seed_any(self, obj: Any) -> None:
        self.seed(self.__class__.PythonObjectEncoder(obj))

    def reset(self) -> None:
        self._value = self._seed
        self._position = 0

    def _enzyme(self, data: Buffer) -> list[int]:
        l = []
        with BytesIO(data) as io:
            while data := io.read1(8):
                l.append(int.from_bytes(data))
        return l

    def _salt(self, rel: int = 0) -> int:
        return _SALT[(self._position + rel)%_SALT_LEN]

    def _combine(self, *data: int) -> None:
        q = self._value
        t = self._salt()
        for d in data:
            t ^= (t >> 32) ^ self._salt()
            q ^= (d >> (t & 0x3f)) ^ (d >> ((t>>16) & 0x3f)) ^ (d >> ((t>>32) & 0x3f)) ^ (d >> ((t>>48) & 0x3f))
            q ^= (self._salt(((q >> 8) ^ (t >> 55))) & q) * (d >> 32) * (q >> 48)
            q ^= d * self._salt(2 + (t & 0x2a))
            q *= d ^ self._salt(7 + (t & 0xe7))
            q ^= (q >> 32) * ((~q) >> 32)
            q &= CONST_UINT64_MAX
            self._position += 1
        self._value = q
        self._position %= _SALT_LEN
        return

    def combine(self, data: Buffer) -> Self:
        self._combine(*self._enzyme(data))
        return self

    def combine_any(self, obj: Any) -> Self:
        return self.combine(self.__class__.PythonObjectEncoder(obj))

    def digest(self, *, reset: bool = False) -> IntRepr:
        q = self._value

        q ^= (
            ((q >> 16) * self._salt(5))
            ^ ((q >> 20) * self._salt(6))
            ^ ((q >> 8) * self._salt(7))
        )
        q ^= ((q >> 34) * self._salt(1)) ^ ((q >> 36) * self._salt(4))
        q ^= self._salt(8) * ~q
        q &= CONST_UINT64_MAX
        q ^= (
            ((q >> 8) * self._salt(9))
            ^ ((q >> 16) * self._salt(10))
            ^ ((q >> 2) * self._salt(11))
            ^ ((q >> 9) * self._salt(12))
        )
        q ^= (
            ((q >> 18) * self._salt(1))
            ^ ((q >> 22) * self._salt(6))
            ^ ((q >> 10) * self._salt(9))
        )
        q ^= self._salt(7) * ~q
        q &= CONST_UINT64_MAX
        q ^= (
            ((q >> 4) * self._salt(13))
            ^ ((q >> 20) * self._salt(14))
            ^ ((q >> 1) * self._salt(15))
        )
        q ^= ((q >> 38) * self._salt(5)) ^ ((q >> 40) * self._salt(13))
        q ^= self._seed
        q &= CONST_UINT64_MAX

        if reset:
            self.reset()

        return IntRepr(q)

    @property
    def value(self) -> IntRepr:
        return IntRepr(self._value)

    # Unique outputs for >1 billion tested calls
    def next(self) -> Self:
        self._combine(self.digest())
        return self

    def __str__(self) -> str:
        return str(self._value)

class IntRepr(int):
    def to_int(self, max: int = CONST_UINT64_MAX) -> int:
        return self % (max + 1)
    def to_float(self, max: int = CONST_UINT64_MAX) -> float:
        """Returns a float value between [0,1)"""
        return (self % (max+1)) / (max+1)

    def to_float_unilateral(self, max: int = CONST_UINT64_MAX) -> float:
        """Returns a float value between [0,1)"""
        return abs(self % (max+1)) / (max+1)

    def to_float_bilateral(self, max: int = CONST_UINT64_MAX) -> float:
        """Returns a float value between [-1,+1]"""
        return (abs(self % (max+1))<<1)/max - 1


class SeededHash():
    ...

    def __init__(self) -> None:
        self._value = 0
        self._ingredients = 0
        self._components = 0
        self._stirs = 0

    def __seasoning(self, i: int=0) -> int:
        return _SALT[(self._stirs+i)%_SALT_LEN] ^ self._stirs ^ (~self._components) ^ (~(self._ingredients<<8)>>8)

    def __stir(self, item: int):
        s = self.__seasoning()
        a,b = (s >> 48) & 0x1f, (s >> 16) & 0x1f
        self._value ^= item
        self._value ^= ((~self._value)>>a) * (self._value>>b) *  ((( s)*(~a)*( b)) ^ ( item))
        self._value ^= ((~self._value)>>b) * (self._value>>a) * ~(((~s)*( a)*(~b)) ^ (~item))
        self._value ^= ~item
        self._stirs += 1

    def __add(self, *items: int) -> None:
        self._stirs = 0
        for item in items:
            self.__stir(item)
            self._components += 1
        self._value ^= self.__seasoning(-1) ^ self.__seasoning(1)

    def mix(self, *ingredients: Any) -> Self:
        for ingredient in ingredients: 
            self.__add(*self.__wash(ingredient))
            self._ingredients += 1
        return self

    @classmethod
    def __scrub(cls, buffer: Buffer) -> Iterable[int]:
        data = []
        with BytesIO(buffer) as io:
            while bytes := io.read1(8):
                data.append(int.from_bytes(bytes))
        return data

    @classmethod
    def __wash(cls, ingredient: Any) -> Iterable[int]:
        if isinstance(ingredient, int):
            return (ingredient,)
        if isinstance(ingredient, Buffer):
            return cls.__scrub(ingredient)

        if isinstance(ingredient, str):
            return cls.__scrub(ingredient.encode())
        elif isinstance(ingredient, float):
            return cls.__scrub(c_double(ingredient))
        elif isinstance(ingredient, complex):
            return cls.__struct_wash(b'complex', c_double, ingredient.real, ingredient.imag)
        elif isinstance(ingredient, slice):
            return cls.__struct_wash(b'slice', c_int64, ingredient.start, ingredient.stop, ingredient.step)
        elif isinstance(ingredient, set):
            ...

        raise TypeError()

    @classmethod
    def __struct_wash[T](cls, name: bytes, item_type: Callable[[T], Buffer], *items: T) -> Iterable[int]:
        arr = bytearray(name)
        for i in items:
            arr+=item_type(i)
        return cls.__scrub(arr)

TAG_INT = b'i'
TAG_BYTE = b'b'
TAG_LEN = b'l'
TAG_BUFFER = b'B'
TAG_STRING = b's'
TAG_FLOAT = b'f'
TAG_COMPLEX = b'c'
TAG_SLICE = b'S'
TAG_SET = b'u'
TAG_ARRAY = b'a'
class Encoder:

    @classmethod
    def gettypecode(cls, tp: type[Any]) -> bytes:
        if tp is int:
            return TAG_INT
        if tp in (bool, c_byte, c_ubyte, c_uint8, c_int8):
            return TAG_BYTE
        if tp in (c_int16, c_uint16):
            return TAG_LEN
        if tp is str:
            return TAG_STRING
        if tp in (set, frozenset):
            return TAG_SET
        if tp is slice:
            return TAG_SLICE
        if tp is complex:
            return TAG_COMPLEX
        if tp in (float, c_float, c_double):
            return TAG_FLOAT
        if tp in (list, tuple):
            return TAG_ARRAY
        return b'x' #unknown
        
    
    @classmethod
    def scrub(cls, buffer: Buffer) -> Iterable[int]:
        data = []
        with BytesIO(buffer) as io:
            while bytes := io.read1(8):
                data.append(int.from_bytes(bytes))
        return data

    @classmethod
    def encode(cls, obj: Any) -> Buffer:
        if isinstance(obj, Buffer):
            return obj
        elif isinstance(obj, (int, bool)):
            return c_int64(obj)
        elif isinstance(obj, str):
            return obj.encode()
        elif isinstance(obj, float):
            return c_double(obj)
        elif isinstance(obj, complex):
            return cls.__struct(b'complex', obj.real, obj.imag)
        elif isinstance(obj, slice):
            return cls.__struct(b'slice', obj.start, obj.stop, obj.step)
        elif isinstance(obj, (set, frozenset)):
            return cls.__struct(b'set', c_uint8(len(obj)), *sorted(obj))
        elif isinstance(obj, (list, tuple)):
            return cls.__struct(b'arr', c_uint8(len(obj)), *obj)
        raise TypeError()

    @classmethod
    def inner_encode(cls, obj: Any) -> Buffer:
        tp = cls.gettypecode(type(obj))

        raise NotImplementedError

    @classmethod
    def __struct(cls, name: bytes, *items: Any, sep: bytes = b'') -> Buffer:
        arr = bytearray(name)
        for i in items:
            arr += cls.encode(i)
            arr += sep
        return arr

    @classmethod
    def __lengthencoded(cls, *values: Any) -> Buffer:
        value = cls.__struct(b'', *values)
        return cls.__struct(b'', c_uint16(memoryview(value).nbytes), value)

    @classmethod
    def __kvp(cls, key: Any, value: Any) -> Buffer:
        return cls.__struct(b'kvp', cls.__lengthencoded(key), cls.__lengthencoded(value))