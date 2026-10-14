from collections.abc import Callable
from datetime import date
from typing import Dict

from holidays.countries.united_states import UnitedStates

from .service import Service
from .timed_service import TimedService

Services: Dict[str, Service] = {
    "H0":
    Service("Hand Rub (5 Min)", 4, cat=["hands"]),
    "H1":
    Service("Hand Rub (10 Min)", 7, cat=["hands"]),
    "HA":
    Service("Hand & Arm Rub (30 Min)", 19, cat=["hands"]),
    "F0":
    Service("Foot Rub (5 Min)", 3, cat=["feet"]),
    "F1":
    Service("Foot Rub (10 Min)", 5, cat=["feet"]),
    "FL":
    Service("Foot & Leg Rub (30 Min)", 13, cat=["feet"]),
    "S0":
    Service("Shoulder Rub (5 Min)", 5, cat=["shoulders"]),
    "S1":
    Service("Shoulder Rub (10 Min)", 9, cat=["shoulders"]),
    "S2":
    Service("Shoulder Rub (30 Min)", 25, cat=["shoulders"]),
    "HF":
    Service("Hands & Feet (10 Min Each)", 11, cat=["hands", "feet"]),
    "FS":
    Service("Feet & Shoulders (10 Min Each)", 13, cat=["feet", "shoulders"]),
    "Ro":
    Service("Royal Massage (10 Min Each [All Types])",
            20,
            cat=["hands", "feet", "shoulders"]),
    "Br":
    Service("Breakfast In Bed", 10, cat=["other"]),
    "Er":
    TimedService("Errand Run (30 Min max)", 3, 0.5, 30),
    "Ub":
    TimedService("Personal Uber (To and From)", 5, 0.2)
}


def getPercentDiscounts() -> float:
    """
    Returns decimal percent discount
    """
    _hols = UnitedStates().get_list(date.today())
    _perc = 0.0
    if "new_years_day" in _hols:
        _perc += 0.1
    if "valentines_day" in _hols:
        _perc += 0.1
    if "april_fools_day" in _hols:
        _perc += 0.05
    if "easter_sunday" in _hols:
        _perc += 0.25
    if "mothers_day" in _hols:
        _perc += 0.25
    if "fathers_day" in _hols:
        _perc += 0.1
    if "labor_day" in _hols:
        _perc += 0.5
    if "halloween" in _hols:
        _perc += 0.1
    if "election_day" in _hols:
        _perc += 0.2
    if "thanksgiving" in _hols:
        _perc += 0.33
    if "christmas_eve" in _hols:
        _perc += 0.5
    if "christmas_day" in _hols:
        _perc += 0.5
    return _perc


def getWholeDiscounts(svc: str, byol: bool = False, byom: bool = False) -> int:
    """
    Returns whole integer discount
    """
    _whol = 0
    if svc in Services:
        _svc = Services[svc]
        if byom and "shoulders" in _svc.category:
            _whol += 1
        if byol and "feet" in _svc.category:
            _whol += 1
        if byol and "hands" in _svc.category:
            _whol += 1
    return _whol


def getDiscountFx(svc: str,
                  birthday: date,
                  byol: bool = False,
                  byom: bool = False) -> Callable[[int], int]:
    """
    Returns discount function
    """
    if svc not in Services:
        return lambda _: 0
    _perM = 1 - getPercentDiscounts()
    _whol = getWholeDiscounts(svc, byol, byom)
    _bdaM = 0.8 if date.today() == birthday else 1.0
    _svc = Services[svc]
    if "timed" not in _svc.category:
        _dis = int((_svc.calc() * _perM - _whol) * _bdaM)
        return lambda _: _dis
    return lambda minutes: int((_svc.calc(minutes) * _perM - _whol) * _bdaM)
