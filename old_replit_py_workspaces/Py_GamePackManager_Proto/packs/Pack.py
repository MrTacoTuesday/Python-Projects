from os.path import join

from packs.datatypes.Manifest import Manifest
from utilities.Folder import Folder


class Pack():

    def __init__(self, *path: str):
        self.path = join(*path)
        root = Folder(self.path)
        self.__load__(root)
        root._forget()

    def __load__(self, root: Folder):
        self.manifest = (root.getFile("manifest.json").ifPresent(
            lambda file: Manifest.fromdata(file.loadContents()),
            returns=Manifest)).forceCast()

    def __str__(self):
        return f"""{self.__class__.__name__}(
    Name \"{self.manifest.name}\"
    Version {self.manifest.version}
    ID {self.manifest.id}
)"""
