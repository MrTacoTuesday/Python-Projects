from re import match
from typing import Any


class Version():

    @staticmethod
    def fromstr(version: str) -> "Version":
        _ = match(r"^\[(\d+)\,\s*(\d+)\,\s*(\d+)\]$", version)
        if not _ or len(_.groups()) not in (2, 3):
            raise ValueError("Invalid version string",
                             "Expected '[major, minor(, patch)]'")
        return Version(*(int(k) for k in _.groups()))

    @staticmethod
    def fromdata(version: Any) -> "Version":
        if isinstance(version, str):
            return Version.fromstr(version)
        elif isinstance(version, list):
            if len(version) not in (2, 3):
                raise ValueError("Invalid version list",
                                 "Expected '[major, minor(, patch)]'")
            return Version(*(int(k) for k in version))
        else:
            raise ValueError("Invalid version",
                             "Expected '[major, minor(, patch)]'")

    @staticmethod
    def is_valid(version: Any) -> bool:
        try:
            return Version.fromdata(version) is not None
        except Exception:
            return False

    def __init__(self, maj: int, min: int, patch: int = 0) -> None:
        self.major = maj
        self.minor = min
        self.patch = patch

    def __repr__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __lt__(self, other: "Version") -> bool:
        if self.major < other.major:
            return True
        elif self.major == other.major:
            if self.minor < other.minor:
                return True
            elif self.minor == other.minor:
                return self.patch < other.patch
        return False

    def __eq__(self, other: "Version") -> bool:
        return (self.major == other.major and self.minor == other.minor
                and self.patch == other.patch)

    def __gt__(self, other: "Version") -> bool:
        if self.major > other.major:
            return True
        elif self.major == other.major:
            if self.minor > other.minor:
                return True
            elif self.minor == other.minor:
                return self.patch > other.patch
        return False

    def __ne__(self, other: "Version") -> bool:
        return not self.__eq__(other)

    def __le__(self, other: "Version") -> bool:
        return not self.__gt__(other)

    def __ge__(self, other: "Version") -> bool:
        return not self.__lt__(other)
