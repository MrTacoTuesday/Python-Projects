from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.Helper import Helper
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.BehaviorPack import BehaviorPack
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.datatypes.UniqueID import UniqueID
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.Pack import Pack
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.ResourcePack import ResourcePack


class PackManager():

    __all_resources__: dict[UniqueID, ResourcePack] = {}
    __active_resources__: list[UniqueID] = []
    __all_behaviors__: dict[UniqueID, BehaviorPack] = {}
    __active_behaviors__: list[UniqueID] = []
    __local_resources__: list[ResourcePack] = []

    @staticmethod
    def loadGlobals():
        PackManager.__all_resources__ = Helper.load_resource_packs(
            ".", "game", "resource_packs")
        PackManager.__all_behaviors__ = Helper.load_behavior_packs(
            ".", "game", "behavior_packs")
        PackManager.setActiveResource(
            UniqueID("0a8ee0e0-d9f6-42a2-b5a2-c010e872bb7a"))
        PackManager.setActiveBehavior(
            UniqueID("0a8ee0e0-d9f6-42a2-b5a2-c010e872bb7a"))

    @staticmethod
    def checkDependencies(pack: Pack) -> bool:
        return (Helper.testDependencies(pack.manifest.dependencies,
                                        PackManager.__all_resources__,
                                        PackManager.__all_behaviors__))

    @staticmethod
    def setActiveResource(uid: UniqueID):
        if uid not in PackManager.__all_resources__:
            return Helper.warning(f"Resource pack with id {uid} not found")
        if uid in PackManager.__active_resources__:
            return Helper.warning(
                f"Resource pack with id {uid} is already active")
        if not PackManager.checkDependencies(
                PackManager.__all_resources__[uid]):
            return Helper.warning(
                f"Resource pack with id {uid} has dependencies which are not loaded"
            )
        PackManager.__active_resources__.append(uid)
        for dep in PackManager.__all_resources__[
                uid].manifest.dependencies.values():
            if dep.type == "resource" and PackManager.getActiveResource(
                    uid) is None:
                PackManager.setActiveResource(uid)
            elif dep.type == "behavior" and PackManager.getActiveBehavior(
                    uid) is None:
                PackManager.setActiveBehavior(uid)

    @staticmethod
    def getActiveResource(uid: UniqueID) -> ResourcePack | None:
        if uid in PackManager.__active_resources__:
            return PackManager.__all_resources__[uid]
        return None

    @staticmethod
    def getActiveResources() -> list[ResourcePack]:
        return [
            PackManager.__all_resources__[uid]
            for uid in PackManager.__active_resources__
        ]

    @staticmethod
    def setActiveBehavior(uid: UniqueID):
        if uid not in PackManager.__all_behaviors__:
            return Helper.warning(f"Behavior pack with id {uid} not found")
        if uid in PackManager.__active_behaviors__:
            return Helper.warning(
                f"Behavior pack with id {uid} is already active")
        if not PackManager.checkDependencies(
                PackManager.__all_behaviors__[uid]):
            return Helper.warning(
                f"Behavior pack with id {uid} has dependencies which are not loaded"
            )
        PackManager.__active_behaviors__.append(uid)
        for dep in PackManager.__all_behaviors__[
                uid].manifest.dependencies.values():
            if dep.type == "resource" and PackManager.getActiveResource(
                    uid) is None:
                PackManager.setActiveResource(uid)
            elif dep.type == "behavior" and PackManager.getActiveBehavior(
                    uid) is None:
                PackManager.setActiveBehavior(uid)

    @staticmethod
    def getActiveBehavior(uid: UniqueID) -> BehaviorPack | None:
        if uid in PackManager.__active_behaviors__:
            return PackManager.__all_behaviors__[uid]
        return None

    @staticmethod
    def getActiveBehaviors() -> list[BehaviorPack]:
        return [
            PackManager.__all_behaviors__[uid]
            for uid in PackManager.__active_behaviors__
        ]
