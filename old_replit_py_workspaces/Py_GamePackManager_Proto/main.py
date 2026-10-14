from types import coroutine

from Helper import Helper
from packs.PackManager import PackManager
from registry.Locale import Locale
from utilities.File import File

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
