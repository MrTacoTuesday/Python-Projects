from typing import Dict


def load(file: str) -> Dict[str, str]:
    d: Dict[str, str] = {}
    with open(file) as f:
        s = f.read().split("\n")
        for S in s:
            if "=" not in S:
                continue
            (key, value) = S.split("=")
            d[key] = value
    #print(d)
    return d