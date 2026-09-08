from abc import abstractmethod
from ctypes import c_double, c_int, c_ubyte
from typing import ClassVar, Iterable, TypeAlias
from collections.abc import Buffer


byteslike: TypeAlias = bytes | bytearray | memoryview
BufferLike: TypeAlias = byteslike | Buffer

class Element[Data, Encoding : BufferLike = BufferLike]:

    @abstractmethod
    def __init__(self, data: Data) -> None: ...

    def writeinto(self, buffer: Bytes) -> None:
        buffer.write(self.encode())

    @abstractmethod
    def encode(self) -> Encoding: 
        raise NotImplementedError

    def __buffer__(self, flags: int) -> memoryview:
        return self.encode().__buffer__(flags)

ReadOnlyError = RuntimeError
class Box[T]:
    READONLY: ClassVar[bool] = True
    def __init__(self, data: T) -> None:
        self._data = data

    @property
    def data(self) -> T:
        return self._data

    @data.setter
    def data(self, value: T) -> None:
        if self.__class__.READONLY:
            raise ReadOnlyError
        self._data = value

class Struct[Data, Encoding: BufferLike = BufferLike](Element[Data, Encoding]):
    TYPECODE: ClassVar[bytes]

    def encode_structure(self) -> BytesArray:
        return BytesArray((self.TYPECODE, self.encode()))

class VariableLengthStruct[Data, Encoding: BufferLike = BufferLike](Struct[Data,Encoding]):
    def encode_structure(self) -> BytesArray:
        data = self.encode()
        length = memoryview(data).nbytes
        lenlen = (length.bit_length()+7)>>3
        return BytesArray((
            self.TYPECODE, 
            c_ubyte(lenlen), length.to_bytes(lenlen), 
            data
        ))

class Bytes(bytearray, VariableLengthStruct[BufferLike | Element, bytearray]):
    TYPECODE = b'\x00'

    def write(self, data: BufferLike | Element) -> None:
        if isinstance(data, Element):
            data.writeinto(self)
        if isinstance(data, Buffer):
            self.__iadd__(data)
        else:
            self.extend(data)

    def encode(self) -> bytearray:
        return self

NONE: Struct[BufferLike, bytearray] = Bytes()

class Integer(int, Struct[int | bool, bytes]):
    TYPECODE = b'\x01'

    def encode(self) -> bytes:
        return memoryview(c_int(self)).tobytes()

class Float(float, Struct[float, bytes]):
    TYPECODE = b'\x02'

    def encode(self) -> bytes:
        return memoryview(c_double(self)).tobytes()

class String(str, Struct[str, bytes]):
    TYPECODE = b'\x03'

    __new__ = str.__new__

    def __init__(self, data: str) -> None:
        ...

class Collection[Data: Element | BufferLike = Element | BufferLike](Iterable[Data], VariableLengthStruct[Iterable[Data], Bytes]):
    IS_ORDERED: ClassVar[bool]

    def encode(self) -> Bytes:
        self.writeinto(buffer := Bytes())
        return buffer

    def writeinto(self, buffer: Bytes) -> None:
        if not self.IS_ORDERED:
            bytesarray = BytesArray(*self)
            bytesarray.sort(key=bytes)
            bytesarray.writeinto(buffer)
        else:
            for item in self:
                buffer.write(item)

class OrderedCollection[Data: Element | BufferLike = Element | BufferLike](list[Data], Collection[Data]):
    TYPECODE = b'\x04'
    IS_ORDERED = True

    def writeinto(self, buffer: Bytes) -> None:
        for item in self:
            buffer.write(item)
Array = List = Tuple = OrderedCollection
BytesArray = Array[Element | BufferLike]

class UnorderedCollection[Data: Element | BufferLike = Element | BufferLike](list[Data], Collection[Data]):
    TYPECODE = b'\x05'
    IS_ORDERED = False

    def writeinto(self, buffer: Bytes) -> None:
        bytesarray = BytesArray(*self)
        bytesarray.sort(key=bytes)
        bytesarray.writeinto(buffer)
Set = FrozenSet = UnorderedCollection

class Complex(complex, Struct[complex, bytes]):
    TYPECODE = b'\x06'

    def encode(self) -> bytes:
        ... 


data = String("hello world")
print(data, data.encode_structure())