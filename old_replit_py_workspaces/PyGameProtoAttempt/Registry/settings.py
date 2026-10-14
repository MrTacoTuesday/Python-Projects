from Registry.locale import Locale
from Registry.utils import load


class Settings:
    language: Locale
    
    @staticmethod
    def load():
        d = load("./game/settings")
        for k in d:
            if k == "language":
                Settings.language = Locale(d[k])