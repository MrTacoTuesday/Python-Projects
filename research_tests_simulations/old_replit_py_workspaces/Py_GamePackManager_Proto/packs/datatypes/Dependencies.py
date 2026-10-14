import json
from typing import Any

from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.datatypes.Dependency import Dependency, Operands, Types
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.datatypes.UniqueID import UniqueID
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.datatypes.Version import Version


class Dependencies(dict[UniqueID, Dependency]):

    @staticmethod
    def fromdata(dependencies: Any) -> "Dependencies":
        if isinstance(dependencies, str):
            dependencies = json.loads(dependencies)
        if isinstance(dependencies, dict):
            d = Dependencies()
            for k, v in dependencies.items():
                if isinstance(k, str):
                    k = UniqueID.fromstr(k)
                if not isinstance(k, UniqueID):
                    raise TypeError(f"Expected UniqueID str, got {type(k)}")
                if not (isinstance(v, list) and len(v) in (2, 3)
                        and v[0] in ["resource", "behavior"]):
                    raise ValueError(
                        "Invalid data length or type",
                        "Expected '[type, version(, operation)]'",
                        "Where type is 'resource' or 'behavior'")
                if not Version.is_valid(v[1]):
                    raise ValueError(
                        "Invalid version",
                        "Expected version='[major, minor(, patch)]'")
                ptype: Types = v[0]
                ver: Version = Version.fromdata(v[1])
                op: Operands = v[2] if len(v) == 3 else ">="
                if op not in ["<", ">", "=", "<=", ">=", "!"]:
                    raise ValueError("Invalid operation",
                                     "Expected '<, >, =, <=, >=, !'")
                d[k] = Dependency(k, ver, ptype, op)
            return d
        raise TypeError("Expected dict or json str")
