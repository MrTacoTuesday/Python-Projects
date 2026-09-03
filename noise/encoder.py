from typing import TypeAlias


byteslike: TypeAlias = bytes | bytearray | memoryview



class _node[Type]:

    @property
    def contents(self) -> Type: ...

    def encode(self, data: Type) -> byteslike: ...


class BYTES(bytearray, _node[byteslike]):

    def __init__(self, contents: byteslike | None = None) -> None:
        if contents is None:
            bytearray.__init__(self)
        else:
            bytearray.__init__(self, contents)



