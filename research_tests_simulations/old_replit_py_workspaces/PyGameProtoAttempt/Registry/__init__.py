from research_tests_simulations.old_replit_py_workspaces.PyGameProtoAttempt.Registry.locale_marker import LocaleMarker
from research_tests_simulations.old_replit_py_workspaces.PyGameProtoAttempt.Registry.settings import Settings

Settings.load()


def getLocalName(locale: str | LocaleMarker)->str:
    if isinstance(locale, str):
        locale = LocaleMarker(locale)
    return locale.search()
