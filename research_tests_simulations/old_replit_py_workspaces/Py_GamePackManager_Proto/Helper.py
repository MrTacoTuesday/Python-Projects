from typing import final

from typing_extensions import Never

from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.BehaviorPack import BehaviorPack
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.datatypes.Dependencies import Dependencies
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.datatypes.UniqueID import UniqueID
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.ResourcePack import ResourcePack
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.utilities.Folder import Folder
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.utilities.typing.Optional import Optional

import time


@final
class Helper():

    @staticmethod
    def load_resource_packs(*path: str) -> dict[UniqueID, ResourcePack]:
        """
        Loads all resource packs in the game's resource pack folder.
        Returns an empty list if the folder at the specified path doesn't exist.
        """
        dir = Optional[Folder].trying(lambda: Folder(*path))
        if not dir.isPresent():
            return {}
        dir = dir.forceCast()
        resource_packs: dict[UniqueID, ResourcePack] = {}
        for pack in dir.folderNames:
            _ = ResourcePack(*path, pack)
            Helper.log(
                f"Loading Resource Pack '{_.manifest.name}' from {_.path}")
            id = _.manifest.id
            if id in resource_packs:
                Helper.warning(
                    f"Error while loading Resource Pack '{_.manifest.name}':",
                    f"Multiple packs with same id ({id}) exist", "Ignoring...")
            resource_packs[id] = _
        dir._forget()
        return resource_packs

    @staticmethod
    def load_behavior_packs(*path: str) -> dict[UniqueID, BehaviorPack]:
        """
        Loads all behavior packs in the game's behavior pack folder.
        Returns an empty list if the folder at the specified path doesn't exist.
        """
        dir = Optional[Folder].trying(lambda: Folder(*path))
        if not dir.isPresent():
            return {}
        dir = dir.forceCast()
        behavior_packs: dict[UniqueID, BehaviorPack] = {}
        for pack in dir.folderNames:
            _ = BehaviorPack(*path, pack)
            Helper.log(
                f"Loading Behavior Pack '{_.manifest.name}' from {_.path}")
            id = _.manifest.id
            if id in behavior_packs:
                Helper.warning(
                    f"Error while loading Behavior Pack '{_.manifest.name}':",
                    f"Multiple packs with same id ({id}) exist", "Ignoring...")
            behavior_packs[id] = _
        dir._forget()
        return behavior_packs

    @staticmethod
    def testDependencies(deps: Dependencies, resources: dict[UniqueID,
                                                             ResourcePack],
                         behaviors: dict[UniqueID, BehaviorPack]) -> bool:
        """
        Tests if all dependencies are met by the given packs.
        """
        if len(deps) == 0:
            return True
        for dep in deps.values():
            if (dep.type == "resource"):
                if (dep.uuid in resources and dep.checkVersion(
                        resources[dep.uuid].manifest.version)):
                    continue
                return False
            elif (dep.type == "behavior"):
                if (dep.uuid in behaviors and dep.checkVersion(
                        behaviors[dep.uuid].manifest.version)):
                    continue
                return False
        return True

    @staticmethod
    def warning(*contents: object) -> None:
        """
        Will be useful later once I implement Error Log Messages
        (like minecraft has up top). Currently just details an exception.
        """
        print("\33[2;31m[Warning]", *contents, "\33[0m")

    @staticmethod
    def fatalError(*contents: object, code: int = 1) -> Never:
        """
        Crashes the game with an error message.
        """
        print("\33[31m{Fatal Error}", *contents, "\33[0m")
        exit(code)

    @staticmethod
    def log(*contents: object) -> None:
        """
        Will be useful later once I implement Log Messages
        (like minecraft has up top). Currently just prints to console.
        """
        print("\33[30m[Info]", *contents, "\33[0m")

    @staticmethod
    def sleep(secs: float) -> None:
        time.sleep(secs)