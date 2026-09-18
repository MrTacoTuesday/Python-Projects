from ctypes import Array, c_uint64
from io import BytesIO
from operator import index
from random import Random
from typing import Any, Iterable, Self, SupportsIndex
from typing_extensions import Buffer

from research_tests_simulations.encoder import v5 as encoder

CONST_UINT64_MAX = 0xFFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF

__all__: list[str] = ['encoder', 'buffer_to_uint64_iterable', 'any_to_uint64_iterable', 'SeededHash', 'HashRandom']


def buffer_to_uint64_iterable(buffer: Buffer) -> Iterable[int]:
    data = []
    with BytesIO(buffer) as io:
        while bytes := io.read1(8):
            data.append(int.from_bytes(bytes, byteorder="big", signed=False))
    return data


def any_to_uint64_iterable(*args: Any, **kwargs: Any) -> Iterable[int]:
    return buffer_to_uint64_iterable(encoder.encode(*args, **kwargs))


_SEASONINGS = (
    0x301226781111FAEE,0xDECE101852E33B31,0x6459F065E91B8408,0x62C7698F19AD5C27,0x474EBAFAE938C63E,0xC4B1826AD1D42696,0x7909BB6B4260ED07,0x274AC0AED25DCB73,
    0x83AEC6080C63B230,0x5AFDDDC100001D63,0x901E6B6A65A5F832,0xB78878ADDDA0A3F5,0x0EA48AC48EAA2488,0x3091FFA56E139233,0x9B361E270A2607EB,0x0E9B710875FE1CEE,
    0x8A5A2938E5C41938,0xEC469FCB2FBF2D57,0x49E2C4047E3CD8E6,0x81F94F2B1753DBC3,0x42B804233456956A,0x25A68DED8C00CD53,0x83DD22BC414F5A64,0xD24E92867640AEBA,
    0x1180F7A66964BEED,0x4B84EB07A3E4896C,0x752DBA7812998CAA,0x161B4B24F31E3FE6,0xBA425ED1C85A44D8,0x3EE633F35F7D40DC,0xF18D10F0FDAEED0E,0x4A244D63308EBC91,
)
_SEASONINGS_LEN: int = len(_SEASONINGS)


class SeededHash:

    def __init__(self, *, seed: Any = None, size: SupportsIndex = 1) -> None:
        self._SIZE: int = index(size)
        self.setseed(seed)

    def setseed(self, seed: Any) -> Self:
        self.__raw: Array[c_uint64] = (c_uint64 * self._SIZE)()
        self.__ingredients = 0
        self.__components = 0
        self.__stirs = 0
        self.__seed = seed
        self.process(seed)
        return self

    def reset(self) -> Self:
        return self.setseed(self.__seed)

    def getseed(self) -> Any:
        return self.__seed

    def __seasoning(self, i: int = 0) -> int:
        return (
            _SEASONINGS[(self.__stirs + i) % _SEASONINGS_LEN]
            ^ self.__stirs
            ^ (~self.__components)
            ^ (~(self.__ingredients << 8) >> 8)
        ) & CONST_UINT64_MAX

    @property
    def __index(self) -> int:
        return self.__stirs + self.__components + self.__ingredients

    @property
    def __cell(self) -> int:
        return self.__raw[self.__index % self._SIZE]

    @__cell.setter
    def __cell(self, value: int) -> None:
        self.__raw[self.__index % self._SIZE] = c_uint64(value)

    def __scramble(self, cell: int, item: int) -> int:
        s: int = self.__seasoning()
        a, b = (s >> 48) & 0x1F, (s >> 16) & 0x1F
        cell ^= item
        cell ^= (
            ((~cell) >> a) * (cell >> b) * (((s) * (~a) * (b)) ^ (item))
        )
        cell ^= (
            ((~cell) >> b)
            * (cell >> a)
            * ~(((~s) * (a) * (~b)) ^ (~item))
        )
        cell ^= ~item
        return cell

    def __add(self, *items: int) -> None:
        self.__stirs = 0
        for item in items:
            self.__cell = self.__scramble(self.__cell, item)
            self.__stirs += 1
            self.__components += 1
        self.__cell ^= self.__scramble(self.__cell, self.__seasoning(-1) ^ self.__seasoning(1))
        self.__stirs = 0

    def __process(self, *items: int) -> None:
        self.__add(*items)
        self.__ingredients += 1

    def process(self, *ingredients: Any) -> Self:
        for ingredient in ingredients:
            self.__process(*any_to_uint64_iterable(ingredient))
        return self

    def digest(self, *, i: int = 0, resets: bool = False) -> int:
        i += self.__index
        q = 0

        for j in range(self._SIZE):
            q ^= self.__raw[(i + j) % self._SIZE]

            s: int = self.__seasoning()
            a, b = (s >> 20) & 0x1F, (s >> 16) & 0x1F

            q ^= (
                ((q >> b) * self.__seasoning(j + 5))
                ^ ((q >> a) * self.__seasoning(j + 6))
                ^ ((q >> 8) * self.__seasoning(j + 7))
            )
            q ^= ((q >> 34) * self.__seasoning(1)) ^ (
                (q >> (a+b)) * self.__seasoning(j + 4)
            )
            q ^= self.__seasoning(j + 8) * ~q
            q ^= self.__scramble(self.__cell, q * s)
            q &= CONST_UINT64_MAX

            q ^= (
                ((q >> 8) * self.__seasoning(j + 9))
                ^ ((q >> b) * self.__seasoning(j + 10))
                ^ ((q >> 2) * self.__seasoning(j + 11))
                ^ ((q >> 9) * self.__seasoning(j + 12))
            )
            q ^= (
                ((q >> 18) * self.__seasoning(j + 1))
                ^ ((q >> 22) * self.__seasoning(j + 6))
                ^ ((q >> 10) * self.__seasoning(j + 9))
            )
            q ^= self.__seasoning(j + 7) * ~q
            q ^= self.__scramble(self.__cell, q * s)
            q &= CONST_UINT64_MAX
            q ^= (
                ((q >> 4) * self.__seasoning(j + 13))
                ^ ((q >> a) * self.__seasoning(j + 14))
                ^ ((q >> 1) * self.__seasoning(j + 15))
            )
            q ^= ((q >> 38) * self.__seasoning(j + 5)) ^ (
                (q >> 40) * self.__seasoning(j + 13)
            )
            q ^= self.__scramble(q, self.__cell * s)
            q &= CONST_UINT64_MAX

        if resets:
            self.reset()

        return q

    def __getstate__(self) -> object:
        return {
            "SIZE": self._SIZE,
            "ingredients": self.__ingredients,
            "components": self.__components,
            "stirs": self.__stirs,
            "seed": self.__seed,
            "raw": bytes(self.__raw),
        }

    def __setstate__(self, state: object) -> None:
        if isinstance(state, dict):
            if not (
                ("SIZE", "ingredients", "components", "stirs", "seed", "raw") in state
            ):
                raise ValueError
            if (
                isinstance(size := state.get("SIZE", 1), int)
                and isinstance(ingredients := state.get("ingredients", 0), int)
                and isinstance(components := state.get("components", 0), int)
                and isinstance(stirs := state.get("stirs", 0), int)
                and isinstance(seed := state.get("seed", None), object)
                and isinstance(raw := state.get("raw"), bytes)
            ):
                self._SIZE: int = size
                self.__ingredients: int = ingredients
                self.__components: int = components
                self.__stirs: int = stirs
                self.__seed: object = seed
                self.__raw: Array[c_uint64] = (c_uint64 * size).from_buffer_copy(raw)
            else:
                raise TypeError
        else:
            raise TypeError

    def nextstate(self) -> Self:
        self.__process(*self.__raw, self.digest())
        return self

    def __bytes__(self) -> bytes:
        return bytes(self.__raw)

    def __buffer__(self, flags: int, /) -> memoryview:
        return self.__raw.__buffer__(flags)

    def __repr__(self) -> str:
        return self.__class__.__qualname__ + f'{{{bytes(self)}}}'


class HashRandom(SeededHash, Random):

    def __init__(self, seed: Any = None, *, size: SupportsIndex = 16) -> None:
        super().__init__(seed=seed, size=size)
        self._bits_used = 0

    def setseed(self, seed: Any) -> Self:
        self._bits_used = 0
        return super().setseed(seed).process(_SEASONINGS_LEN, *_SEASONINGS)

    def seed(self, a: Any = None, version: int | None = None) -> None:
        match version:
            case 0:
                super().setseed(a)
            case 1 | None:
                self.setseed(a)
            case int():
                raise ValueError(version)
            case _:
                raise TypeError(version)

    def bit_length(self) -> int:
        return self._SIZE * 64

    def nextstate(self) -> Self:
        self._bits_used = 0
        return super().nextstate()

    ## TODO: FIXME: currently produces unique, random (avg 0.5) values, but is quite slow
    def getrandbits(self, k: int) -> int:
        if k == 0:
            return 0

        l = self.bit_length()

        b = self._bits_used
        data = int.from_bytes(self, byteorder='big', signed=False)>>b
        b = data.bit_length()

        while b < k:
            data <<= l
            b += l
            data ^= int.from_bytes(self.nextstate(), byteorder='big', signed=False)
        if b > k:
            self._bits_used = b-k
            data >>= self._bits_used
        return data
    
    def random(self) -> float:
        """Generates a random float in the range [0,1]"""
        from math import ldexp
        mantissa: int = 0x10_0000_0000_0000 | self.getrandbits(52)
        exponent = -53
        x = 0
        while not x:
            x: int = self.getrandbits(32)
            exponent += x.bit_length() - 32
        return ldexp(mantissa, exponent)

    def randbool(self) -> bool:
        return bool(self.getrandbits(1))

    def randchance(self, probability: float = 0.5) -> bool:
        return self.random() < probability