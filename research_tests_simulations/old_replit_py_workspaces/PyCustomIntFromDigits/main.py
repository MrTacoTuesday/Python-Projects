from research_tests_simulations.old_replit_py_workspaces.PyCustomIntFromDigits.Int import Int

_p, _m = -123456, 176
p, m = Int.parse(_p), Int.parse(_m)

print(p.quorem(m))

for k, v in {
    "p": (p, ),
    "m": (m, ),
    "p+m": (p+m, _p+_m),
    "p-m": (p-m, _p-_m),
    "m-p": (m-p, _m-_p),
    "p*m": (p*m, _p*_m),
    "p//m": (p//m, round(_p/_m)),
    "p%m": (p%m, abs(_p)%_m),
    }.items():
        print(f"{k:>6} = {v[0]:10d}", end="")
        if len(v) == 2:
            print(f" [{v[1]:11d}]", end="")
        print()



"""

    FIXME:

        ...

"""