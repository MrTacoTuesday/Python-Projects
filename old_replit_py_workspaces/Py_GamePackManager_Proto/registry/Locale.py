from typing import Literal

from packs.datatypes.LocaleData import LocaleData
from packs.PackManager import PackManager
from packs.ResourcePack import ResourcePack
from utilities.typing.Optional import Optional

Region = Literal["en_US"]


class Locale():

    __loaded__: "dict[Region, Locale]" = {}

    def __class_getitem__(cls, item: Region) -> "Locale":
        if item not in cls.__loaded__:
            cls.__loaded__[item] = Locale(item)
        return cls.__loaded__[item]

    @classmethod
    def updateAll(cls) -> None:
        for locale in cls.__loaded__.values():
            locale.loadFromGlobalResources()
            locale.__local_data__ = LocaleData()

    @classmethod
    def dataFrom(cls, packs: list[ResourcePack]) -> dict[str, LocaleData]:
        d: dict[str, LocaleData] = {}
        for rp in reversed(packs):
            data = rp.regions.orElse({})
            for region in data:
                if region not in d:
                    d[region] = data[region]
                else:
                    d[region].update(data[region])
        return d

    def __init__(self, region: Region) -> None:
        self.region = region
        self.__global_data__: LocaleData = LocaleData()
        self.__local_data__: LocaleData = LocaleData()

    def loadFromGlobalResources(self) -> None:
        self.__global_data__ = self.dataFrom(
            PackManager.getActiveResources()).get(self.region, LocaleData())

    def loadFromLocalResources(self) -> None:
        pass

    def __repr__(self) -> str:
        return (f"Locale[{self.region}]")

    def __getitem__(self, key: str) -> Optional[str]:
        val = None
        if key in self.__local_data__:
            val = self.__local_data__.get(key)
        elif key in self.__global_data__:
            val = self.__global_data__.get(key)
        return Optional[str].assign(val)

    def get(self, key: str) -> str:
        return self[key].orElse(key)
