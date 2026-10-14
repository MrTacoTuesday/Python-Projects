import re
from typing import Any

from packs.datatypes.parse_string import parse_string


class LocaleData(dict[str, str]):

    @staticmethod
    def fromdata(data: Any) -> "LocaleData":
        if isinstance(data, dict):
            if not all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in data.items()):
                raise TypeError("LocaleData pairs must be of {(str): (str)}")
            return LocaleData(data)
        elif isinstance(data, str):
            d = LocaleData()
            for line in data.split("\n"):
                if line.startswith("#") or line.isspace() or line == "":
                    continue
                match = re.match(r"^\s*(.+)\s*=\s*(.+)$", line)
                if match:
                    k, v = match.groups()
                    d[k.rstrip(" ")] = parse_string(v)
                    continue
                raise (ValueError(
                    f"Expected format 'name = value': \n\tGot '{line}'"))
            return d
        raise TypeError(f"Expected dict or str, got {type(data).__name__}")
