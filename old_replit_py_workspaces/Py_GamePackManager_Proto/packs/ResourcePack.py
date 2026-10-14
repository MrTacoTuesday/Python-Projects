from packs.datatypes.LocaleData import LocaleData
from packs.Pack import Pack
from utilities.Folder import Folder


class ResourcePack(Pack):

    def __load__(self, root: Folder):
        super().__load__(root)
        self.regions = root.getFolder("regions").ifPresent(
            lambda folder: {
                name: LocaleData.fromdata(
                    folder.getFile(name).ifPresent(
                        lambda file: file.loadContents(), returns=str))
                for name in folder.fileNames
            },
            returns=dict[str, LocaleData])
