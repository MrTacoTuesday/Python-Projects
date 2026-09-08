from collections.abc import Buffer
from ctypes import c_double
from enum import ReprEnum
from types import FunctionType, MethodType
from typing import Any, ClassVar, Iterable, SupportsIndex
from typing_extensions import Self

DEFAULT_OBJECT_DIRECTORY = frozenset(type.__dir__(object))
DEFAULT_TYPE_DIRECTORY = frozenset(type.__dir__(type)) - DEFAULT_OBJECT_DIRECTORY
class _provider:
    ...
DEFAULT_CLASS_DIRECTORY = frozenset(type.__dir__(_provider)) - DEFAULT_OBJECT_DIRECTORY - DEFAULT_TYPE_DIRECTORY
del _provider

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

debug(DEFAULT_CLASS_DIRECTORY)

class Typecode(bytes, ReprEnum):
    Bytes = b'\x00'
    Integer = b'\x01'
    FloatingPoint = b'\x02'
    String = b'\x03'
    KeyValuePair = b'\x04'
    Sequence = b'\x05'
    Set = b'\x06'
    Mapping = b'\x07'


class _encodes:
    def encode(self) -> bytes:
        raise NotImplementedError

def _encode(t: Typecode, d: Buffer) -> bytes:
    if not isinstance(d, (bytes, bytearray)):
        d = bytes(d)
    return t + len(d).to_bytes(7) + d
def _encode_generic(o: Any) -> bytes:
    if isinstance(o, _encodes):
        return o.encode()
    

    raise NotImplementedError

class Bytes(bytes, _encodes): 
    def encode(self) -> bytes:
        return _encode(Typecode.Bytes, self)
class Integer(int, _encodes):
    def encode(self) -> bytes:
        return _encode(Typecode.Integer, self.to_bytes((self.bit_length()+7)>>3, signed=True))
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
            result += _encode_generic(item)
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
            segments.append(i.to_bytes(3) + _encode_generic(item))
        if not self.Ordered:
            segments.sort()
        return _encode(self.Typecode, sum(segments, b''))
class Mapping(dict[Any, Any], _encodes):
    def encode(self) -> bytes:
        segments: list[bytes] = []
        for item in self.items():
            segments.append(KeyValuePair(item).encode())
        segments.sort()
        return _encode(Typecode.Mapping, sum(segments, b''))

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

def get_object_data(o: object):
    typ = type(o)
    cls = getattr(o, '__origin__', getattr(o, '__orig_class__', getattr(o, '__class__', None)))
    bases = tuple(getattr(o, '__orig_bases__', getattr(o, '__bases__', ())))
    attrs = set(getattr(o, '__static_attributes__', None) or ())
    slots = set(getattr(o, '__slots__', None) or ())
    dct = get_object_dict(o)
    return (typ, cls, bases, attrs, slots, dct,)

def get_object_dict(o: object):
    return {k:v for k,v in getattr(o, '__dict__', {}).items() if k not in (
        '__firstlineno__', '__type_params__', '__annotate_func__', '__orig_class__', '__dict__', '__weakref__', '__origin__', '__orig_bases__', '__static_attributes__', '__slots__', '__class__', '__bases__'
    )}

def get_function_data(f: FunctionType | MethodType):
    closure = f.__closure__
    if closure: 
        closure = b'@' + bytes(closure[0].cell_contents.__qualname__, 'utf-8')
    else:
        closure = b''
    return (f.__name__.encode()+closure+f.__code__.co_code)


def get_object_state(o: object, reduce_protocol_version: SupportsIndex = 5):
    tp = type(o)
    state = tp.__getstate__(o)
    if state is not None:
        # class instance with data
        debug(state)
        return tp.__reduce_ex__(o, reduce_protocol_version)[1:]
    else:
        debug(o)
        debug(tp.__reduce_ex__(o, 5))
        ... # is struct data type? get superclass & raw value





o = wrapper(21)
debug(get_object_data(o))
debug(get_object_state(o))
o = wrapper
debug(get_object_data(o))
debug(get_object_state(o))

class ObjectState(dict[str, Any]):
    def __init__(self, iterable: Iterable[tuple[str, Any]]) -> None:
        dict(iterable)
    def __repr__(self) -> str:
        for k in (set(self)-DEFAULT_OBJECT_DIRECTORY):
