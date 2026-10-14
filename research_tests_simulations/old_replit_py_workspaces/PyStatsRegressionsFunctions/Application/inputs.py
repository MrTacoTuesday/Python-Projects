from collections.abc import Callable


def input_integer(prompt: str = " >> ",
                  failure: str | None = None,
                  min: int | None = None,
                  max: int | None = None,
                  padding: int = 0) -> int:
    n = ""
    while not str.isdigit(n):
        n = input(padding * "\t" + prompt)
        if not str.isdigit(n) and failure:
            print(padding * "\t" + "\t" + failure)
        elif str.isdigit(n) and min and int(n) < min:
            print(padding * "\t" + "\t" + "Value must be >= " + str(min))
            n = ""
        elif str.isdigit(n) and max and int(n) > max:
            print(padding * "\t" + "\t" + "Value must be <= " + str(max))
            n = ""
    return int(n)


def input_float(prompt: str = " >> ",
                failure: str | None = None,
                min: float | None = None,
                max: float | None = None,
                padding: int = 0) -> float:
    n = ""
    while not str.isdecimal(n):
        n = input(padding * "\t" + prompt)
        if not str.isdecimal(n) and failure:
            print(padding * "\t" + "\t" + failure)
        elif str.isdecimal(n) and min and float(n) < min:
            print(padding * "\t" + "\t" + "Value must be >= " + str(min))
            n = ""
        elif str.isdecimal(n) and max and float(n) > max:
            print(padding * "\t" + "\t" + "Value must be <= " + str(max))
            n = ""
    return float(n)


def input_string(prompt: str = " >> ",
                 failure: str | None = None,
                 isValid: Callable[[str], bool] = lambda s: s != "",
                 padding: int = 0) -> str:
    n = ""
    while isValid(n):
        n = input(padding * "\t" + prompt)
        if not isValid(n) and failure:
            print(padding * "\t" + "\t" + failure)
    return n


def input_function(prompt: str = " >> ",
                 failure: str | None = None,
                 padding: int = 0) -> Callable:
    n = ""
    while n == "":
        n = input(padding * "\t" + prompt)
        if n == "" and failure:
            print(padding * "\t" + "\t" + failure)
        elif n != "":
            try:
                eval(n)
            except Exception as _:
                print(padding * "\t" + "\tInvalid Function")
    return lambda: eval(n)
