from Registry.settings import Settings


class LocaleMarker:
    def __init__(self, tag: str) -> None:
        self.tag = tag

    def search(self) -> str:
        return Settings.language.getName(self.tag)
