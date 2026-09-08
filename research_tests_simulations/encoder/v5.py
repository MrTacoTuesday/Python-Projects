from abc import ABC, abstractmethod
from collections.abc import Buffer
from ctypes import c_double
from enum import ReprEnum
from types import BuiltinFunctionType, BuiltinMethodType, ClassMethodDescriptorType, FunctionType, GetSetDescriptorType, MappingProxyType, MemberDescriptorType, MethodDescriptorType, MethodType, MethodWrapperType, WrapperDescriptorType
from typing import Any, ClassVar, Iterable, SupportsIndex
from typing_extensions import Self

DEFAULT_OBJECT_DIRECTORY = frozenset(type.__dir__(object))

def debug(
    *values: object,
    sep: str | None = " ",
    end: str | None = "\n\n",
    file: Any | None = None,
    flush: bool = False
) -> None: 
    if __name__ == '__main__':
        print(*values, sep=sep, end=end, file=file, flush=flush)
    else:
        ...

class Typecode(bytes, ReprEnum):
    Bytes = b'\x00'
    Integer = b'\x01'
    FloatingPoint = b'\x02'
    String = b'\x03'
    KeyValuePair = b'\x04'
    Sequence = b'\x05'
    Set = b'\x06'
    Mapping = b'\x07'
    Function = b'\x08'
    Type = b'\x09'
    Object = b'\x0a'


class _encodes(ABC):
    def encode(self) -> bytes:
        raise NotImplementedError

def _encode(t: Typecode, d: Buffer) -> bytes:
    if not isinstance(d, (bytes, bytearray)):
        d = bytes(d)
    l = len(d)
    lb = (l.bit_length()+7)>>3
    return t + lb.to_bytes() + l.to_bytes(lb) + d

def _encode_generic(o: Any) -> bytes:
    return Object.parse(o).encode()

class Bytes(bytes, _encodes): 
    def encode(self) -> bytes:
        return _encode(Typecode.Bytes, self)
class Integer(int, _encodes):
    def encode(self) -> bytes:
        try:
            return _encode(Typecode.Integer, self.to_bytes((self.bit_length()+7)>>3, signed=True))
        except:
            return _encode(Typecode.Integer, self.to_bytes((self.bit_length()+7)>>3, signed=False))
class FloatingPoint(float, _encodes):
    def encode(self) -> bytes:
        return _encode(Typecode.FloatingPoint, c_double(self))
class String(str, _encodes):
    def encode(self, encoding: str = "utf-8", errors: str = "strict") -> bytes:
        return _encode(Typecode.String, super().encode(encoding, errors))
class KeyValuePair(tuple[Any, Any], _encodes):
    def encode(self) -> bytes:
        result = Typecode.KeyValuePair
        for item in self:
            result += Object.parse(item).encode()
        return result
class Collection(tuple[Any, ...], _encodes):
    Ordered: ClassVar[bool]
    def __new__(cls, iterable: Iterable[Any] = ()) -> Self:
        cls.Ordered = not isinstance(iterable, (set, dict))
        cls.Typecode = Typecode.Sequence if cls.Ordered else Typecode.Set
        return super().__new__(cls, iterable)
    def encode(self) -> bytes:
        segments: list[bytes] = []
        for i, item in enumerate(self):
            segments.append(i.to_bytes(3) + Object.parse(item).encode())
        if not self.Ordered:
            segments.sort()
        return _encode(self.Typecode, b''.join(segments))
class Mapping(dict[Any, Any], _encodes):
    def encode(self) -> bytes:
        segments: list[bytes] = []
        for item in self.items():
            segments.append(KeyValuePair(item).encode())
        segments.sort()
        return _encode(Typecode.Mapping, b''.join(segments))
class Function(_encodes):
    def __init__(self, func: FunctionType | MethodType | WrapperDescriptorType):
        self.func = func
    def encode(self) -> bytes:
        try:
            closure = getattr(self.func, '__closure__', None) or b''
            if closure: 
                closure = b'@' + bytes(closure[0].cell_contents.__qualname__, 'utf-8')
            closure += getattr(self.func, '__code__.co_code', b'')
        except:
            closure = b'<unknown>'
        return _encode(Typecode.Function, self.func.__name__.encode()+closure)
    def __repr__(self) -> str:
        return repr(self.func)
class Object(_encodes):
    @classmethod
    def parse(cls, o: Any) -> _encodes:
        if isinstance(o, _encodes):
            return o
        tp = type(o)
        if tp in (bytes, memoryview, bytearray):
            return Bytes(o)
        if tp in (int, bool):
            return Integer(o)
        if tp in (float,):
            return FloatingPoint(o)
        if tp in (str,):
            return String(o)
        if tp in (tuple, list, set, frozenset):
            return Collection(o)
        if tp in (dict, MappingProxyType):
            return Mapping(o)
        if tp in (
            FunctionType, MethodType, BuiltinFunctionType, 
            BuiltinMethodType, WrapperDescriptorType, MethodDescriptorType, 
            MethodWrapperType, ClassMethodDescriptorType, GetSetDescriptorType, MemberDescriptorType):
            return Function(o)
        
        return Object(o)

    def __init__(self, value: object):
        self.obj = value
        self.Typecode = Typecode.Type if isinstance(value, type) else Typecode.Object
    def origin(self) -> type[Any]:
        return getattr(self.obj, '__origin__', getattr(self.obj, '__orig_class__', getattr(self.obj, '__class__', type(self.obj))))
    def bases(self) -> tuple[type[Any], ...]:
        return tuple(getattr(self.obj, '__orig_bases__', getattr(self.obj, '__bases__', ())))
    def attributes(self) -> set[str]:
        return set(getattr(self.obj, '__static_attributes__', None) or ()) | set(getattr(self.obj, '__slots__', None) or ())
    def dict(self) -> dict[str, Any]:
        return {k: getattr(self.obj, k, None) for k in dir(self.obj) if k not in DEFAULT_OBJECT_DIRECTORY}
    def encode(self) -> bytes:
        if self.obj is None:
            data = b''
        elif self.obj in (object, type):
            data = b'\x00'
        else:
            data = Mapping({
                b'origi': self.origin(),
                b'bases': self.bases(),
                b'attrs': self.attributes(),
                b'dicti': self.dict()
            }).encode()
        return _encode(self.Typecode, data)

    def __repr__(self) -> str:
        if self.obj in (None, object, type):
            return repr(self.obj)
        else:
            return repr({
                'origi': self.origin(),
                'bases': self.bases(),
                'attrs': self.attributes(),
                'dicti': self.dict()
            })

# [type]{1 byte}[data-size]{3 bytes}[data]{data-size bytes}

# EX: 
# ('a': 'Hello, World!')
# [KeyValuePair][size: 2][item: 0]{[String][size: 1][data: b'a']}[item 1:]{[String][size: 13][data: b'Hello, World!']}


class wrapper[T](int):
    z: ClassVar[int] = 82
    w: ClassVar[int]
    a: T
    b: int = 18

    def __new__(cls, arg: T):
        cls.a = arg
        return super().__new__(cls)

    def __init__(self, arg: T, *, y: int = 10) -> None:
        self.argument = arg
        self.x = 0
        self.y = y


o = wrapper(21)
debug(Object.parse(o).encode())
o = wrapper
debug(Object.parse(o).encode())