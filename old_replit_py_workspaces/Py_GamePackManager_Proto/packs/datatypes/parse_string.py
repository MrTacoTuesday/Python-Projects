import re


def parse_string(data: str) -> str:
    if not re.match(r"\"(.+)\"+$", data):
        return data
    return data[1:-1].replace("\\n", "\n").replace("\\t", "\t")
