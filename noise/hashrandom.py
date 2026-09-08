from ctypes import c_uint64
from io import BytesIO
from operator import index
from random import Random
from typing import Any, Iterable, Self, SupportsIndex
from typing_extensions import Buffer

CONST_UINT64_MAX = 0xFFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF


def buffer_to_uint64_iterable(buffer: Buffer) -> Iterable[int]:
    data = []
    with BytesIO(buffer) as io:
        while bytes := io.read1(8):
            data.append(int.from_bytes(bytes, byteorder="big", signed=False))
    return data


def any_to_uint64_iterable(*args: Any, **kwargs: Any) -> Iterable[int]:
    from research_tests_simulations.encoder.v5 import encode

    return buffer_to_uint64_iterable(encode(*args, **kwargs))


_SEASONINGS = (
    0x301226781111FAEE,0xDECE101852E33B31,0x6459F065E91B8408,0x62C7698F19AD5C27,0x474EBAFAE938C63E,0xC4B1826AD1D42696,0x7909BB6B4260ED07,0x274AC0AED25DCB73,
    0x83AEC6080C63B230,0x5AFDDDC100001D63,0x901E6B6A65A5F832,0xB78878ADDDA0A3F5,0x0EA48AC48EAA2488,0x3091FFA56E139233,0x9B361E270A2607EB,0x0E9B710875FE1CEE,
    0x8A5A2938E5C41938,0xEC469FCB2FBF2D57,0x49E2C4047E3CD8E6,0x81F94F2B1753DBC3,0x42B804233456956A,0x25A68DED8C00CD53,0x83DD22BC414F5A64,0xD24E92867640AEBA,
    0x1180F7A66964BEED,0x4B84EB07A3E4896C,0x752DBA7812998CAA,0x161B4B24F31E3FE6,0xBA425ED1C85A44D8,0x3EE633F35F7D40DC,0xF18D10F0FDAEED0E,0x4A244D63308EBC91,
)
_SEASONINGS_LEN = len(_SEASONINGS)


class SeededHash:

    def __init__(self, *, seed: Any = None, size: SupportsIndex = 1) -> None:
        self.__SIZE = index(size)
        self.setseed(seed)

    def setseed(self, seed: Any) -> Self:
        self.__raw = (c_uint64 * self.__SIZE)()
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
        )

    @property
    def __index(self) -> int:
        return self.__stirs + self.__components + self.__ingredients

    @property
    def __cell(self) -> int:
        return self.__raw[self.__index % self.__SIZE].value

    @__cell.setter
    def __cell(self, value: int):
        self.__raw[self.__index % self.__SIZE] = c_uint64(value)

    def __scramble(self, item: int):
        s = self.__seasoning()
        a, b = (s >> 48) & 0x1F, (s >> 16) & 0x1F
        self.__cell ^= item
        self.__cell ^= (
            ((~self.__cell) >> a) * (self.__cell >> b) * (((s) * (~a) * (b)) ^ (item))
        )
        self.__cell ^= (
            ((~self.__cell) >> b)
            * (self.__cell >> a)
            * ~(((~s) * (a) * (~b)) ^ (~item))
        )
        self.__cell ^= ~item
        self.__stirs += 1

    def __add(self, *items: int) -> None:
        self.__stirs = 0
        for item in items:
            self.__scramble(item)
            self.__components += 1
        self.__cell ^= self.__seasoning(-1) ^ self.__seasoning(1)

    def process(self, *ingredients: Any) -> Self:
        for ingredient in ingredients:
            self.__add(*any_to_uint64_iterable(ingredient))
            self.__ingredients += 1
        return self

    def digest(self, *, resets: bool = False) -> int:
        i = self.__index
        q = 0

        for j in range(self.__SIZE):
            q ^= self.__raw[(i + j) % self.__SIZE]

            q ^= (
                ((q >> 16) * self.__seasoning(j + 5))
                ^ ((q >> 20) * self.__seasoning(j + 6))
                ^ ((q >> 8) * self.__seasoning(j + 7))
            )
            q ^= ((q >> 34) * self.__seasoning(1)) ^ (
                (q >> 36) * self.__seasoning(j + 4)
            )
            q ^= self.__seasoning(j + 8) * ~q
            q &= CONST_UINT64_MAX
            q ^= (
                ((q >> 8) * self.__seasoning(j + 9))
                ^ ((q >> 16) * self.__seasoning(j + 10))
                ^ ((q >> 2) * self.__seasoning(j + 11))
                ^ ((q >> 9) * self.__seasoning(j + 12))
            )
            q ^= (
                ((q >> 18) * self.__seasoning(j + 1))
                ^ ((q >> 22) * self.__seasoning(j + 6))
                ^ ((q >> 10) * self.__seasoning(j + 9))
            )
            q ^= self.__seasoning(j + 7) * ~q
            q &= CONST_UINT64_MAX
            q ^= (
                ((q >> 4) * self.__seasoning(j + 13))
                ^ ((q >> 20) * self.__seasoning(j + 14))
                ^ ((q >> 1) * self.__seasoning(j + 15))
            )
            q ^= ((q >> 38) * self.__seasoning(j + 5)) ^ (
                (q >> 40) * self.__seasoning(j + 13)
            )
            q &= CONST_UINT64_MAX

        if resets:
            self.reset()

        return q

    def __getstate__(self) -> object:
        return {
            "SIZE": self.__SIZE,
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
                self.__SIZE = size
                self.__ingredients = ingredients
                self.__components = components
                self.__stirs = stirs
                self.__seed = seed
                self.__raw = (c_uint64 * size).from_buffer_copy(raw)
            else:
                raise TypeError
        else:
            raise TypeError

    def nextstate(self) -> Self:
        return self.process(self.digest())

    def __bytes__(self) -> bytes:
        return bytes(self.__raw)

    def __repr__(self) -> str:
        return super().__repr__() + f'{{{bytes(self)}}}'


class HashRandom(SeededHash, Random):

    def __init__(self, *, seed: Any = None, size: SupportsIndex = 16) -> None:
        super().__init__(seed=seed, size=size)

    def setseed(self, seed: Any) -> Self:
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
        return self.__SIZE * 64

    def getrandbits(self, k: int) -> int:
        data = bytes(self)
        while (len(data)<<3) < k:
            data += bytes(self.nextstate())
        else:
            self.nextstate()
        return int.from_bytes(data, byteorder='big', signed=False) & (1<<k)

    def random(self) -> float:
        """Generates a random float in the range [0,1]"""
        from math import ldexp
        mantissa = 0x10_0000_0000_0000 | self.getrandbits(52)
        exponent = -53
        x = 0
        while not x:
            x = self.getrandbits(32)
            exponent += x.bit_length() - 32
        return ldexp(mantissa, exponent)

    def randbool(self) -> bool:
        return bool(self.getrandbits(1))

    def randchance(self, chance: float = 0.5) -> bool:
        return super().random() < chance
