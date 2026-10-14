from math import pi, sqrt
from typing import List, Tuple

from research_tests_simulations.old_replit_py_workspaces.Py_Candy_JobQuote_GuessCalc.constants import (
    MATS_NOT_PROVIDED,
    MATS_PROVIDED,
    MOWER_PUSH,
    MOWER_RIDING,
    MOWER_WEEDEATER,
)
from research_tests_simulations.old_replit_py_workspaces.Py_Candy_JobQuote_GuessCalc.utils import cprint

#### LAWN MOWING CALCULATIONS ####


def mowing_time_approx_original(acres: float,
                                mower: int = MOWER_RIDING) -> float:
    return 2.6203 * acres * (3.125)**mower


def mowing_time_approx_realistic(
    acres: float,
    mower_deck_ft: float,
    mph: float,
) -> float:
    return (acres * 25) / (mower_deck_ft * mph)


def mowing_time_approx(
    acres: float,
    mower_type: int = MOWER_RIDING,
) -> float:
    return acres * 2.45 * 1.77**mower_type


def mowing_cost(
    hours: float,
    acres: float,
    mower: int = MOWER_RIDING,
    mats: bool = MATS_PROVIDED,
) -> float:
    materialCharge = 1.25**abs(not mats)
    timeWage = 7.25 * hours
    areaWage = 45 * acres + 30 * acres * mower**4
    return round(materialCharge * areaWage + timeWage, 2)


def mowing_cost_approx(
    acres: float,
    mower: int = MOWER_RIDING,
    mats: bool = MATS_PROVIDED,
) -> float:
    return mowing_cost(mowing_time_approx(acres, mower), acres, mower, mats)


def job(
    sections: List[Tuple[float, int]],
    isFamily: bool = False,
    mats: bool = MATS_NOT_PROVIDED,
) -> float:
    subtotal = 0 if mats or isFamily else 15
    for section in sections:
        acres = section[0]
        mower = section[1]
        t = 0 if isFamily else mowing_time_approx(acres, mower)
        subtotal += mowing_cost(t, acres, mower, mats)
    return round(subtotal)


#### CANDY IN JAR CALCULATIONS ####


def volume_candy_piece(a: float, b: float, c: float) -> float:
    Vs = pi * a * b * c / 4
    return Vs


Vs = volume_candy_piece


def volume_candy_space(a: float, b: float, c: float) -> float:
    Vsp = 2.1850556771978 * Vs(a, b, c)
    ##print(Vsp)
    return Vsp


Vsp = volume_candy_space


def volume_candy(a: float, b: float, c: float) -> float:
    ##print("Vc", Vs(a,b,c), Vsp(a,b,c))
    Vc = Vs(a, b, c) + Vsp(a, b, c)
    ####Vc = pi * Vs(a,b,c)
    ## Vc ≈ 3.18506 * Vs
    ## Vc =? pi * Vs = Vs + (pi-1)*Vs
    return Vc


Vc = volume_candy


def volume_container(diameter: float,
                     height: float,
                     offset: float = 3 / 4) -> float:
    x = diameter / 2 - offset
    y = height - offset
    Vi = pi * (x)**2 * y
    return Vi


Vi = volume_container


def candy_jar_guess(
    piece_dimensions: Tuple[float, float, float],
    container_dimensions: Tuple[float, float],
    container_offset: float = 3 / 4,
) -> Tuple[float, float, float]:
    p = piece_dimensions
    c = container_dimensions
    z = container_offset
    vi = Vi(c[0], c[1], z)
    vc = Vc(p[0], p[1], p[2])
    ml = 0.8 * max((c[1] - 1) / c[1], 0.7)
    mh = 1.0 * min((c[1] + 1) / c[1], 1.3)
    ##print("Volumes", vi, vc)
    ##print("Under/Overestimate", ml, mh)
    med = vi / vc
    MIN = ml * med
    MAX = mh * med
    MED = med * sqrt(mh**2 - ml**2)
    ##print("Data", med, MIN, MAX, MED)
    return (round(MIN), round(MED), round(MAX))
