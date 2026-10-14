from typing_extensions import Self

from research_tests_simulations.old_replit_py_workspaces.PySwiftLangBridge.MAIN.swift.Object import Object, String


class Foo(String):

    def __init__(self: Self, data: str = "Foo") -> None:
        str.__new__(type(self), data)
        self.bar = 7

print(Foo.Self().bar)
print(Foo())

Object()