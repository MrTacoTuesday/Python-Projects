from .locale_data import LocaleData


class Locale:

    REGISTRY: dict[str, LocaleData] = {}

    __current_data: LocaleData
    packs: list[str] = []

    @staticmethod
    def get_name(key: str) -> str:
        return Locale.__current_data.get(key) or Locale.get("en_US").get(
            key) or key

    @staticmethod
    def set_locale(locale: str):
        Locale.__current_data = Locale.get(locale)

    @staticmethod
    def update_packs(packs: list[str]):
        Locale.packs = packs
        Locale.__current_data.update_packs(packs)

    @staticmethod
    def get(locale: str) -> LocaleData:
        if locale not in Locale.REGISTRY:
            Locale.REGISTRY[locale] = LocaleData(locale)
        data = Locale.REGISTRY[locale]
        data.update_packs(Locale.packs)
        return data
