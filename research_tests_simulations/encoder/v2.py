
from abc import abstractmethod
from collections.abc import Buffer as _Buffer, Iterable
from ctypes import c_int64
from io import BytesIO
from typing import Any, Protocol, SupportsBytes, SupportsIndex, TypeAlias



class Box[T]:
    def __init__(self, data: T) -> None:
        self._data = data

    @property
    def data(self) -> T:
        return self._data

BytesConvertible: TypeAlias = SupportsBytes | SupportsIndex | _Buffer | Iterable[SupportsIndex] | str
class Buffer(Box[memoryview], _Buffer):

    def __init__(self, data: BytesConvertible) -> None:
        if isinstance(data, _Buffer):
            pass
        elif isinstance(data, str):
            data = bytes(data, encoding='utf-8')
        else:
            data = bytes(data)
        super().__init__(memoryview(data))

    def __buffer__(self, flags: int) -> memoryview[int]:
        return self.data.__buffer__(flags)



