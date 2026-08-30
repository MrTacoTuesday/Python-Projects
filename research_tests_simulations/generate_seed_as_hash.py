

from datetime import date
from typing import Iterable

def combine(*args, **kwargs) -> int:
    k = 0
    for i in args:
        k ^= hash(i)
    for n,i in kwargs.items():
        if isinstance(i, Iterable):
            i = combine(*i)
        elif isinstance(i, int):
            pass
        else:
            i = hash(i)
        k ^= (hash(n) << 3) & i
    k %= (1<<64)
    k = (k << 32) + (k >> 32)
    return k % (1<<64) - (1<<63)

Ryley = combine(
    name="Ryley Nicole Brooks",
    birthday=date(2005, 7, 11),
    anniversary=date(2025, 3, 7),
    partner="Weston Hunter Chaney",
    church="Trinity Baptist",
    favorite_foods={"Pizza",},
    ring_size=3.75,
    current_series="The Amazing Digital Circus",
    weight="~100lbs"
)

Weston = combine(
    name="Weston Hunter Chaney",
    birthday=date(2005, 11, 28),
    email="westonchaney@outlook.com",
    phone="+17063055293",
    anniversary=date(2025, 3, 7),
    partner="Ryley Nicole Brooks",
    mother="Heidi Lee Baxter Chaney",
    father="Eric Michael Chaney",
    church="Stevens Creek",
    favorite_foods={"Ramen", "Spaghetti",},
    ring_size=10,
    current_series="That Time I Got Reincarnated As A Slime",
    work="Jersey Mike's #5050",
    weight="207.3lbs",
)

Us = combine(Weston=Weston, Ryley=Ryley)
RyleySeeds = combine(
    -2338435250711872642,
    -3046337448406300637,
    -4703347833220351426,
    "ryleyDearest",
    -136075949,
    74717452319542288,
    2180188180146124052,
    743900385354722119,
    1789681472228736224,
    12723534569979378,
    784479831171870151,
    1583722604153279454,
    1051894783068092721,
    7595339538713030543,
    1478596698696460727,
    8896415429349441900,
    8920621805186221601,
    7929461356765105541, #!!!
    7428685793509350334, #!
    7021623957930920333, #!!
    8096347836291901151, #!!
    7203420882311410630, #!!
    8548961368662622043, #!!
    2261762810442215182, #!!
    3020958001574988675, #!!
    -623540482790945213, #!
)
CoolSeeds = combine(
    -1101531943807632616,
    4949538022646618205,
    -136075949,
    1163555988184371568,
    74717452319542288,
    2180188180146124052,
    743900385354722119,
    1789681472228736224,
    8075896670468001700,
    12723534569979378,
    784479831171870151,
    1794697992494803351,
    1911093671620274736,
    1583722604153279454,
    1051894783068092721,
    7595339538713030543,
    1478596698696460727,
    8405139968999928525,
    8896415429349441900,
    8920621805186221601,
    8226112364992912453,
    8146284515391699306,
    7929461356765105541,
    7428685793509350334,
    7021623957930920333,
    8096347836291901151,
    7203420882311410630,
    8548961368662622043,
    2261762810442215182,
    2257293605570300083,
    3020958001574988675,
    -623540482790945213,
)
print()
print(combine(RyleySeeds, ~CoolSeeds, Us, ~Weston | ~Ryley, ~RyleySeeds, CoolSeeds, RyleySeeds, Us, Weston & Ryley))
print()