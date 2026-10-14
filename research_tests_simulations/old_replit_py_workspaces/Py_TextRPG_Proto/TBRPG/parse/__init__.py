from typing import TypeVar


def wait_for_string() -> str:
    cmd = input("\33[2;33m > \33[0;1;35m")
    print("\33[0m")
    return cmd


def wait_for_command() -> list[str]:
    return wait_for_string().split(" ")


def wait_for_number() -> float | int | None:
    num = wait_for_string()
    try:
        float(num)
    except Exception:
        return None
    return int(num) if num.isdigit() else float(num)


def wait_for_integer() -> int | None:
    num = wait_for_number()
    if num is None:
        return None
    if isinstance(num, int):
        return num
    return int(num) if num.is_integer() else None

_V = TypeVar("_V")
def wait_for_registered_item(registry: dict[str, _V]) -> _V:
    key = None
    while key not in registry:
        key = wait_for_string()


def alert(prompt: str):
    print("\33[1;31m{}\33[0m".format(prompt))


def inform(info: str):
    print("\33[1;32m{}\33[0m".format(info))


def whisper(msg: str):
    print("\33[3;34m{}\33[0m".format(msg))
