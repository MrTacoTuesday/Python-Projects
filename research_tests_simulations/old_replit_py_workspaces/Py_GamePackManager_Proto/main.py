from types import coroutine

from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.Helper import Helper
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.packs.PackManager import PackManager
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.registry.Locale import Locale
from research_tests_simulations.old_replit_py_workspaces.Py_GamePackManager_Proto.utilities.File import File

__is_loading: bool = False
__alive: float = 0

@coroutine
def setup():
    global __is_loading
    __is_loading = True
    PackManager.loadGlobals()
    for p in PackManager.getActiveResources():
        print(p)
    l = Locale("en_US")
    l.loadFromGlobalResources()
    print(l.get("attribute.common.dexterity.name"))

    Helper.log("Loading complete!")
    __is_loading = False


print(File.atPath(".", "game", "behavior_packs", "Dev", "manifest.json"))

setup()
print(__alive)
Helper.fatalError("Dogs took over the world.")



"""
TODO:
    - Add file saving system to Folder [DONE]
    - Add Settings
        - Loadable from ./game/settings.json
        - Saveable
"""
