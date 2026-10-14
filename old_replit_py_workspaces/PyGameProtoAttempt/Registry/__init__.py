from Registry.locale_marker import LocaleMarker
from Registry.settings import Settings

Settings.load()


def getLocalName(locale: str | LocaleMarker)->str:
    if isinstance(locale, str):
        locale = LocaleMarker(locale)
    return locale.search()
