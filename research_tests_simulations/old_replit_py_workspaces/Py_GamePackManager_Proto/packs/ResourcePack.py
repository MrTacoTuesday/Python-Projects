from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.datatypes.LocaleData import LocaleData
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.Pack import Pack
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.utilities.Folder import Folder


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
