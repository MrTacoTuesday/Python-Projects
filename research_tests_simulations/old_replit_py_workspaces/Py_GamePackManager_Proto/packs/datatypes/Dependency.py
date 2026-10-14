from typing import Literal
from uuid import UUID

from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.datatypes.Version import Version

Operands = Literal["<", ">", "=", "<=", ">=", "!"]
Types = Literal["resource", "behavior"]


class Dependency():

    def __init__(self,
                 uuid: UUID,
                 version: Version,
                 type: Types,
                 operand: Operands = ">=") -> None:
        self.uuid = uuid
        self.version = version
        self.operand = operand
        self.type = type

    def __str__(self) -> str:
        return f"{self.uuid}: {self.operand}{self.version}"

    def satisfied(self, uuid: UUID, version: Version, type: Types) -> bool:
        if self.uuid == uuid and self.type == type:
            return self.checkVersion(version)
        return False

    def checkVersion(self, version: Version) -> bool:
        if self.operand == "<":
            return version < self.version
        elif self.operand == ">":
            return version > self.version
        elif self.operand == "=":
            return version == self.version
        elif self.operand == "<=":
            return version <= self.version
        elif self.operand == ">=":
            return version >= self.version
        elif self.operand == "!":
            return version != self.version
        return False
