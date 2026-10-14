from os.path import join


class File():

    @staticmethod
    def __load_content__(*path: str) -> str:
        with open(join(*path), "r") as file:
            return file.read()

    @staticmethod
    def __save_content__(content: str, *path: str, flush: bool = True):
        with open(join(*path), "w") as file:
            if flush:
                file.flush()
            file.write(content)

    @staticmethod
    def atPath(*path: str) -> "File":
        return File(path[-1], File.__load_content__(*path), *path[:-1])

    def __init__(self,
                 name: str,
                 contents: str = "",
                 *path: str,
                 loading: bool = False):
        self.__name__ = name
        self.__ext__ = name.split(".")[-1]
        self.__contents__ = contents
        self.__path__: str = join(*path, name)
        if loading:
            self.load()

    def save(self) -> "File":
        """
        Saves the File's contents to the path given in the constuctor

        Returns: This File instance
        """
        File.__save_content__(self.contents, self.path)
        return self

    def append(self, contents: str) -> "File":
        """
        Appends the specified contents to the path given in the constuctor

        Returns: This File instance
        """
        File.__save_content__(contents, self.path, flush=False)
        self.load()
        return self

    def saveAs(self, name: str, *path: str) -> "File":
        """
        Saves the File's contents to the path specified

        Returns: The new File instance with the specified contents
        """
        return File(name, self.contents, *path).save()

    def hold(self, contents: str):
        """
        Updates the contents of the File instance, 
        however it does not alter the actual file
        """
        self.__contents__ = contents

    def holdAt(self, *path: str) -> "File":
        """
        Creates a copied File referencing the path specified,
        but does not alter the actual file

        Returns: A new File instance with the specified path
        """
        return File(self.name, self.contents, *path)

    def load(self):
        """
        Loads the path given in the constuctor and copies the contents
        """
        self.__contents__ = File.__load_content__(self.path)

    @property
    def name(self) -> str:
        """
        The name of the file
        """
        return self.__name__

    @property
    def path(self) -> str:
        """
        The path the file can be found at.
        Cannot be changed, but calling 
        holdAt(path:) will generate a copy at the new path.
        """
        return self.__path__

    @property
    def contents(self) -> str:
        """
        The value that is currently being held 
        as the contents of the file. 
        Can be changed by calling hold(contents:)
        or by calling load() to reload the file from ROM.
        """
        return self.__contents__

    def loadContents(self) -> str:
        """
        Loads and returns the contents of 
        the path given in the constructor.
        """
        self.load()
        return self.__contents__

    def _forget(self):
        """
        Removes this File from RAM.
        """
        del self

    def __repr__(self) -> str:
        return f"""{self.__class__.__name__}@{{{self.__path__}}}(
    name:
        {self.name}
    contents:
        {self.loadContents()}
)"""
