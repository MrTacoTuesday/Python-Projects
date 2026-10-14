from typing import List, Tuple
from functions import candy_jar_guess, job
from utils import cprint, fprint, fstr, get_info_as


def get_candy_dimensions() -> Tuple[float, float, float]:
    fprint([30], "How big is the candy (l, w, h)?")
    a = get_info_as(fstr([3, 35], "1st measurement of the candy: "),
                    valid_in=lambda s: float(eval(s)) > 0,
                    format=lambda s: float(eval(s)))
    b = get_info_as(fstr([3, 35], "2nd measurement of the candy: "),
                    valid_in=lambda s: float(eval(s)) > 0,
                    format=lambda s: float(eval(s)))
    c = get_info_as(fstr([3, 35], "3rd measurement of the candy: "),
                    valid_in=lambda s: float(eval(s)) > 0,
                    format=lambda s: float(eval(s)))
    return (a, b, c)


def get_jar_dimensions() -> Tuple[Tuple[float, float], float]:
    fprint([30], "How big is the jar?")
    d = get_info_as(fstr([3, 35], "Diameter of jar: "),
                    valid_in=lambda s: float(eval(s)) > 0,
                    format=lambda s: float(eval(s)))
    h = get_info_as(fstr([3, 35], "Height of candy in jar: "),
                    valid_in=lambda s: float(eval(s)) > 0,
                    format=lambda s: float(eval(s)))
    z = get_info_as(fstr([3, 35], "Thickness of jar: "),
                    valid_in=lambda s: float(eval(s)) > 0,
                    format=lambda s: float(eval(s)))
    return ((d, h), z)


def get_candy_in_jar() -> Tuple[float, float, float]:
    dim_jar = get_jar_dimensions()
    dim_candy = get_candy_dimensions()
    return candy_jar_guess(dim_candy, dim_jar[0], dim_jar[1])


def do_candy_guess():
    fprint([1, 4, 30], "Time to guess how much candy (or other substance) is in a jar!")
    (min, guess, max) = get_candy_in_jar()
    fprint(
        [2, 32],
        "There should be between", fstr([1,4,31], min, clr=False), "and",
        fstr([1,4,31], max, clr=False), "pieces of candy in the jar")
    fprint(
        [2, 32], 
        "You should guess around", fstr([1,4,33], guess, clr=False), 
        "are in the jar")

def get_section(num: int = 0) -> Tuple[float, int]:
    fprint([30], f"Provide the mower and acreage of section #{num}")
    m = get_info_as(fstr([3, 35], "Mower type (id): "),
                    valid_in=lambda s: int(s) in (0,1,2),
                    format=lambda s: int(s))
    a = get_info_as(fstr([3, 35], "Acreage: "),
                    valid_in=lambda s: float(eval(s)) > 0,
                    format=lambda s: float(eval(s)))
    return (a, m)

def get_sections() -> List[Tuple[float, int]]:
    fprint([31], "MOWER:: Riding: 0, Push: 1, Weed-eater: 2")
    _l = []
    c = True
    while c:
        _l.append(get_section(len(_l)+1))
        c = get_info_as(fstr([3, 30], "Is there another section (Y or Enter)? "),
                    valid_in=lambda s: s in ["Y", ""],
                    format=lambda s: s == "Y")    
    return _l

def get_job_quote() -> float:
    sec = get_sections()
    fd = get_info_as(fstr([3, 35], "Apply family discount (Y or Enter)? "),
                valid_in=lambda s: s in ["Y", ""],
                format=lambda s: s == "Y")
    md = get_info_as(fstr([3, 35], "Apply material discount (Y or Enter)? "),
                valid_in=lambda s: s in ["Y", ""],
                format=lambda s: s == "Y")
    return job(sec, fd, md)

def do_job_quote():
    fprint([1, 4, 30], "Let's estimate the cost of the job!")
    quote = get_job_quote()
    fprint(
        [2, 32], 
        "You should charge around", fstr([1,4,33], f"${quote}", clr=False), 
        "to complete this job")