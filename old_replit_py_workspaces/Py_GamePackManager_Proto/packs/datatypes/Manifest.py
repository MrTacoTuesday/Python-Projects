import json
from typing import Any

from packs.datatypes.Dependencies import Dependencies
from packs.datatypes.GList import GList
from packs.datatypes.UniqueID import UniqueID
from packs.datatypes.Version import Version


class Manifest():

    @staticmethod
    def fromdata(manifest: Any) -> "Manifest":
        data = json.loads(manifest)
        return Manifest(id=UniqueID.fromstr(data.get("pack-id")),
                        name=str(data.get("name", "")),
                        version=Version.fromdata(data.get("version")),
                        description=str(data.get("description", "")),
                        dependencies=Dependencies.fromdata(
                            data.get("dependencies", {})),
                        authors=GList[str].fromdata(data.get("authors", [])),
                        lisence=str(data.get("lisence")))

    def __init__(self,
                 id: UniqueID,
                 version: Version,
                 name: str = "",
                 description: str = "",
                 dependencies: Dependencies | None = None,
                 authors: list[str] | None = None,
                 lisence: str = "None"):
        self.id = id
        self.name = name
        self.version = version
        self.description = description
        self.dependencies = dependencies or Dependencies()
        self.authors = authors or []
        self.lisence = lisence

    def __str__(self):
        return f"""Manifest(
    Name \"{self.name}\"
    Version {self.version}
    ID {self.id}
)"""
