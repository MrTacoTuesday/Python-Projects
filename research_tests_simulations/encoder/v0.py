from collections.abc import Iterable
from ctypes import c_double
from typing import Any



class _bytes(bytearray):
    def __init__(self, *contents: bytes | bytearray, linked_state: bytearray | None = None) -> None:
        if linked_state is None:
            super().__init__()
        else:
            super().__init__(linked_state)
        self.update(*contents)

    def update(self, *contents: bytes | bytearray) -> None:
        for item in contents:
            super().__iadd__(item)

    def payload(self, *, typecode: bytes | bytearray = b'\x00', array: bytearray | None = None) -> _bytes:
        return _bytes(typecode, _integer(len(self)).raw(), self, linked_state=array)
    
class _integer(int):
    def raw(self, signed: bool = False) -> bytes:
        len = (self.bit_length()>>3) + 1
        if len:
            return len.to_bytes() + self.to_bytes(len, signed=signed)
        return len.to_bytes()
    def payload(self, *, array: bytearray | None = None) -> _bytes:
        return _bytes(b'\x01', self.raw(True), linked_state=array)

class _float(float):
    def payload(self, *, array: bytearray | None = None) -> _bytes:
        return _bytes(b'\x02', b'\x01\x08', memoryview(c_double(self)).tobytes(), linked_state=array)

class _str(str):
    def payload(self, *, array: bytearray | None = None) -> _bytes:
        return _bytes(b'\x03', bytearray(self, "utf-8"), linked_state=array)

class _arr[T=Any](list[T]):
    def __init__(self, iterable: Iterable[T], *, typecode: bytes | bytearray, order: bool = False) -> None:
        super().__init__(iterable)
        self.typecode = typecode
        self.order = order

    def payload(self, *, array: bytearray | None = None) -> _bytes:
        if array is None: array = bytearray()
        data = list[_bytes]()
        for x in self:
            data.append(_obj(x).payload())
        if self.order:
            data.sort()
        return _bytes(*data).payload(typecode=self.typecode, array=array)

class _dict(dict[Any, Any]):
    def __init__(self, *items: tuple[Any, Any]) -> None:
        super().__init__(items)

    def payload(self, *, array: bytearray | None = None) -> _bytes:
        if array is None: array = bytearray()
        data = list[_bytes]()
        for i, o in self.items():
            data.append(_bytes())
            _obj(i).payload(array=data[-1])
            _obj(o).payload(array=data[-1])
            print(i, o, data[-1])
        data.sort()
        return _bytes(*data).payload(typecode=b'\x06', array=array)

class _struct(_arr):
    def __init__(self, *items: Any, header: str | bytes | bytearray | _bytes = _bytes(), typecode: bytes | bytearray = b'\x07') -> None:
        super().__init__(items, typecode=typecode, order=False)
        self.header = _str(header).payload() if isinstance(header, str) else header

    def payload(self, *, array: bytearray | None = None) -> _bytes:
        if array is None: array = bytearray()
        data = bytearray(self.header)
        for i, o in zip(range(len(self)), self):
            _integer(i).payload(array=data)
            _obj(o).payload(array=data)
        return _bytes(data).payload(typecode=self.typecode, array=array)



class _obj:
    def __init__(self, value: Any) -> None:
        self.value = value

    @classmethod
    def coalesce(cls, o: Any) -> _bytes | _integer | _float | _str | _arr | _struct | _dict | None:
        if isinstance(o, (_struct, _bytes, _integer, _float, _str, _arr, _dict)):
            return o
        if o is None:
            return _bytes()
        
        if isinstance(o, (bytes, bytearray)):
            return _bytes(o)
        if isinstance(o, (bool, int)):
            return _integer(o)
        if isinstance(o, float):
            return _float(o)
        if isinstance(o, str):
            return _str(o)
        if isinstance(o, (set, frozenset)):
            return _arr(o, typecode=b'\x04', order=True)
        if isinstance(o, (list, tuple)):
            return _arr(o, typecode=b'\x05')
        if isinstance(o, dict):
            return _dict(*o.items())
        if isinstance(o, slice):
            return _struct((o.start, o.stop, o.step), header=slice.__name__)
        if isinstance(o, complex):
            return _struct((o.real, o.imag), header=complex.__name__)
        

    def payload(self, *, array: bytearray | None = None) -> _bytes:
        if array is None: array = bytearray()
        o = _obj.coalesce(self.value)
        print(o, type(o))
        if o is not None:
            return o.payload(array=array)
        return _struct(*self.sectionalize(), typecode=b'\x08').payload(array=array)

    def sectionalize(self, array: bytearray | None = None) -> _struct:
        o = self.value
        if type(o) is object:
            return _struct(b'\x00', b'\x00')
        if type(o) is type:
            return _struct(b'\x00', b'\x01')
        attrs = {
            attr: getattr(o, attr, None) 
            for attr in set(
                getattr(o, '__slots__', ()) + 
                getattr(o, '__static_attributes__', ())
            )
        }
        if isinstance(o, type):
            root = _struct(b'\x01', type(o), _struct(
                o.__qualname__, o.__bases__, o.__doc__, attrs
            ))
        else:
            root =_struct(b'\x02', o.__class__, _struct(
                attrs, o.__doc__
            ))
        return root


    



print(_obj({
    "once": True,
    ("twice", 2): False
}).payload())


class slotted:
    __slots__ = ('a')


    def __init__(self) -> None:
        self.a: int = 8

class dicted():

    def __init__(self) -> None:
        self.b = 10


