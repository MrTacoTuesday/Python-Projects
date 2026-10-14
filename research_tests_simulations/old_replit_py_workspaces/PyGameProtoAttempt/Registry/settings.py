from research_tests_simulations.old_replit_py_workspaces.PyGameProtoAttempt.Registry.locale import Locale
from research_tests_simulations.old_replit_py_workspaces.PyGameProtoAttempt.Registry.utils import load


class Settings:
    language: Locale
    
    @staticmethod
    def load():
        d = load("./game/settings")
        for k in d:
            if k == "language":
                Settings.language = Locale(d[k])