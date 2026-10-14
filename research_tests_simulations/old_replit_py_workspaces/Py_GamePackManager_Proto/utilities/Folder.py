from os import makedirs, pathsep, scandir
from os.path import join

from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.utilities.File import File
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.utilities.typing.Optional import Optional


class Folder():

    def __init__(self, *path: str):
        self.name: str = path[-1].split(pathsep)[-1]
        self.path: str = join(*path)
        self.__files__: dict[str, File] = {}
        self.__folders__: dict[str, Folder] = {}
        self.folderNames: list[str] = []
        self.fileNames: list[str] = []
        for object in scandir(self.path):
            if object.is_dir():
                self.folderNames.append(object.name)
            elif object.is_file():
                self.fileNames.append(object.name)

    def __load_file__(self, name: str):
        with open(join(self.path, name), "r") as file:
            self.__files__[name] = File(name,
                                        file.read(),
                                        self.path,
                                        loading=True)

    def __load_subfolder__(self, name: str):
        self.__folders__[name] = Folder(join(self.path, name))

    def __write_folder__(self, name: str, override: bool):
        if not override and name in self.folderNames:
            return
        self.folderNames.append(name)
        makedirs(join(self.path, name), exist_ok=True)

    def __write_file__(self, name: str, contents: str, override: bool):
        if not override and name in self.fileNames:
            return
        self.fileNames.append(name)
        with open(join(self.path, name), 'w') as f:
            f.write(contents)

    def loadAllFiles(self):
        """
        Loads all files as File objects.
        """
        for name in self.fileNames:
            self.__load_file__(name)

    def loadAllSubfolders(self):
        """
        Loads all folders as Folder objects
        """
        for name in self.folderNames:
            self.__load_subfolder__(name)

    def getFile(self, name: str) -> Optional[File]:
        """
        Get a file by name, if present.
        """
        if name in self.fileNames:
            if name not in self.__files__:
                self.__load_file__(name)
            return Optional[File].assign(self.__files__[name])
        return Optional[File].Empty()

    def makeFile(self,
                 name: str,
                 contents: str = "",
                 override: bool = False) -> File:
        """
        Replaces file if override, creates the file if not present.
        """
        self.__write_file__(name, contents, override)
        return self.__files__[name]

    def copyFile(self, file: File, override: bool = False) -> File:
        """
        Copies a file to the folder.
        """
        return self.makeFile(file.name, file.contents, override)

    def getFolder(self, name: str) -> "Optional[Folder]":
        """
        Get a subfolder by name, if present.
        """
        if name in self.folderNames:
            if name not in self.__folders__:
                self.__load_subfolder__(name)
            return Optional[Folder].assign(self.__folders__[name])
        return Optional[Folder].Empty()

    def makeFolder(self, name: str, override: bool = False) -> "Folder":
        """
        Replaces folder if override, creates the folder if not present.
        """
        self.__write_folder__(name, override)
        return self.__folders__[name]

    def copyFolder(self, folder: "Folder", override: bool = False) -> "Folder":
        """
        Copies a folder into this folder
        """
        self.__write_folder__(folder.name, override)
        _foldr = self.__folders__[folder.name]
        _foldr.copyContentsOf(folder)
        return _foldr

    def copyContentsOf(self,
                       folder: "Folder",
                       override: bool = False) -> "Folder":
        """
        Copies all files and subfolders from the 
        given folder to the root of this folder.
        """
        print("copying files at path", folder.path, "to", self.path)
        for name in folder.fileNames:
            print("\tcopying file", name)
            f = folder.getFile(name)
            if f.isPresent():
                self.copyFile(f.forceCast(), override)
        for name in folder.folderNames:
            print("\tcopying folder", name)
            f = folder.getFolder(name)
            if f.isPresent():
                self.copyFolder(f.forceCast(), override)
        print("finished copying contents of", folder.name)
        return self

    def _forget_children(self):
        """
        Removes all file and folder data from RAM.
        """
        for f in self.__folders__.values():
            f._forget()
        for f in self.__files__.values():
            f._forget()
        self.__files__ = {}
        self.__folders__ = {}

    def _forget(self):
        """
        Removes this Folder and all its data from RAM.
        """
        self._forget_children()
        del self

    def __repr__(self) -> str:
        sep = "\n\t\t"
        return f"""{self.__class__.__name__}@{{{self.path}}}(
    files: 
        {sep.join(self.fileNames)}
    folders: 
        {sep.join(self.folderNames)}
)"""
