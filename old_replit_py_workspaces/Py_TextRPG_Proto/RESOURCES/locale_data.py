import re
from io import TextIOWrapper


class LocaleData:

    def __init__(self, region: str, packs: list[str] | None = None):
        self.region = region
        self.packs = packs or []
        self.terms: dict[str, str] = {}
        self.pack_terms: dict[str, str] = {}
        self.load()
        self.load_packs()

    def load(self):
        with open(f"RESOURCES/regions/{self.region}", "r",
                  encoding="utf-8") as file:
            self.__load_file_contents(file, self.terms)

    def load_packs(self):
        for pack in reversed(self.packs):
            with open(f"{pack}/regions/{self.region}", "r",
                      encoding="utf-8") as file:
                self.__load_file_contents(file, self.pack_terms)

    def __load_file_contents(self, file: TextIOWrapper, into: dict[str, str]):
        while not file.closed:
            line = file.readline()
            if line == "":
                break
            if line.isspace() or line.startswith("#"):
                continue
            splits = re.split(r"\s*=\s*", line)
            if len(splits) < 2:
                continue
            key, value = splits
            if value.endswith("\n"):
                value = value.removesuffix("\n")
            into[key] = value

    def update_packs(self, packs: list[str]):
        self.packs = packs
        self.load_packs()

    def get(self, key: str, default: str | None = None) -> str | None:
        return self.pack_terms.get(key, self.terms.get(key, default))
