from uuid import UUID


class UniqueID(UUID):

    @staticmethod
    def fromstr(uid: str) -> "UniqueID":
        return UniqueID(uid)

    @staticmethod
    def is_valid(uid: str) -> bool:
        try:
            return UniqueID(uid) is not None
        except ValueError:
            return False