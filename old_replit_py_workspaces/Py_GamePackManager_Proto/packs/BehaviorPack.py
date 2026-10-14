from packs.Pack import Pack
from utilities.Folder import Folder


class BehaviorPack(Pack):

    def __load__(self, root: Folder):
        super().__load__(root)
