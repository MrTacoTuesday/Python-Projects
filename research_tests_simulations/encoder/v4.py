from collections.abc import Buffer, Iterable
from ctypes import Union, c_byte, c_double, c_float, c_int16, c_int64, c_int8, c_ubyte, c_uint16, c_uint64, c_uint8
from io import BytesIO
import random
from typing import Any, Self


CONST_MANTISSA_MASK_64 = 0x1f_ffff_ffff_ffff # (1<<53) - 1
CONST_EXPONENT_MASK_64 = 0x7fff
class c_union_double_uint64(Union):
    _fields_ = (
        ('uint64', c_uint64), ('double', c_double)
    )

    def __init__(self, value: float|int) -> None:
        super().__init__(value)

    @property
    def uint64(self) -> c_uint64:
        return super().__getattribute__('uint64')

    @property
    def double(self) -> c_double:
        return super().__getattribute__('float')

    def __repr__(self) -> str:
        return f'flint({self.uint64} or {self.double})'

    def double_get_sign_bit(self) -> bool:
        return bool(self.uint64.value >> 63)

    def double_get_exponent_bits(self) -> int:
        return (self.uint64.value >> 52) & CONST_EXPONENT_MASK_64

    def double_get_mantissa_bits(self) -> int:
        return (self.uint64.value & CONST_MANTISSA_MASK_64)
    def double_get_components(self) -> tuple[bool, int, int]:
        v = self.uint64.value
        return (bool(v>>63), (v>>52)&CONST_EXPONENT_MASK_64, v&CONST_MANTISSA_MASK_64)

    @classmethod
    def make_double_from_components(cls, sign: bool, exponent: int, mantissa: int) -> Self:
        return cls((sign << 63)|((exponent&CONST_EXPONENT_MASK_64)<<52)|(mantissa&CONST_MANTISSA_MASK_64))

# (-1)**raw_sign * 1.raw_mantissa * 2**(raw_exponent-1023)
# (-1)**raw_sign * 0.raw_mantissa * 2**(raw_exponent-1023+1) when raw_exponent=0
#     =     (-1)**raw_sign * 0.raw_mantissa * 2**(-1022)

r = random.random()
print(r, c_union_double_uint64(r).double_get_components())