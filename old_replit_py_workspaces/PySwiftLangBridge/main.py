from typing_extensions import Self

from MAIN.swift.Object import Object, String


class Foo(String):

    def __init__(self: Self, data: str = "Foo") -> None:
        str.__new__(type(self), data)
        self.bar = 7

print(Foo.Self().bar)
print(Foo())

Object()