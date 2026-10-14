


from Application.inputs import input_float, input_integer, input_string
from Stat.data import Data


def data_from_xy() -> Data:

    title = "Data"
    type = None

    _dat = {}

    print("DATA CREATE - COORDS")
    n = input_integer("How many Data values >> ", 
                  failure="Please enter a number.",
                  min = 0, max = 200, padding=1)

    print("\tEnter Data Values")
    for i in range(n):
        x = input_float(f"X{i+1} >> ",
                failure="Please enter a number.",
                padding=2)
        y = input_float(f"Y{i+1} >> ",
                failure="Please enter a number.",
                padding=2)
        _dat[x] = y

    print("\tDONE\n")

    return Data(_dat, title=title, type=type)

def data_from_fx() -> Data:

    title = "Data"
    type = None

    _dat = {}
    x = 0

    print("DATA CREATE - FX")
    fx = input_string("Y = ", 
                  failure="Please enter a python expression.",
                  isValid=lambda s: (
                      eval(s)
                  ), padding=1)

    print("\tEnter Data Values")
    for i in range(n):
        x = input_float(f"X{i+1} >> ",
                failure="Please enter a number.",
                padding=2)
        y = input_float(f"Y{i+1} >> ",
                failure="Please enter a number.",
                padding=2)
        _dat[x] = y

    print("\tDONE\n")

    return Data(_dat, title=title, type=type)


