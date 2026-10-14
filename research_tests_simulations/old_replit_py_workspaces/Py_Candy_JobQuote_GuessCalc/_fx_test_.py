from research_tests_simulations.old_replit_py_workspaces.Py_Candy_JobQuote_GuessCalc.constants import (
    DIM_COOKIE, DIM_KISS, DIM_MALLOW, DIM_OREO, DIM_RCUP,
    DIM_RMINI, MATS_NOT_PROVIDED, MATS_PROVIDED, MOWER_PUSH,
    MOWER_RIDING, MOWER_WEEDEATER)
from research_tests_simulations.old_replit_py_workspaces.Py_Candy_JobQuote_GuessCalc.functions import (candy_jar_guess, job)
from research_tests_simulations.old_replit_py_workspaces.Py_Candy_JobQuote_GuessCalc.utils import (cprint)

#### MOWING JOBS ####

cprint(31, "MOWING JOB QUOTES -> $$")

cprint(32, "\n931 RUST BRANCH LANE JOB")
cprint(
    34, "FRONT, BACK, SIDE;",
    job(
        [
            (0.61, MOWER_RIDING),
            (0.01, MOWER_WEEDEATER),
        ],
        isFamily=True,
        mats=MATS_PROVIDED,
    ))

cprint(32, "\n586 FOXHUNT LANE JOB")
cprint(
    34, "FRONT, COURT, BACK;",
    job(
        [
            (0.26, MOWER_PUSH),
            (0.02, MOWER_PUSH),
            (0.40, MOWER_RIDING),
            (0.10, MOWER_PUSH),
            (0.03, MOWER_WEEDEATER),
        ],
        isFamily=True,
        mats=MATS_PROVIDED,
    ))
cprint(36, "FRONT;",
       job(
           [
               (0.26, MOWER_PUSH),
           ],
           isFamily=True,
           mats=MATS_PROVIDED,
       ))

cprint(32, "\nLAND CLEARING JOB")
cprint(
    34, "A;",
    job([
        (1.2, MOWER_RIDING),
        (0.3, MOWER_PUSH),
        (0.1, MOWER_WEEDEATER),
    ], ))
cprint(34, "B;", job([
    (1, MOWER_RIDING),
], ))

cprint(32, "\n6113 RIDGE ROAD JOB")
cprint(
    34, "FRONT, BACK, SIDE STRIP;",
    job(
        [
            (0.44 * 0.97, MOWER_RIDING),
            (0.44 * 0.03, MOWER_PUSH),
            (0.06, MOWER_WEEDEATER),
        ],
        isFamily=True,
        mats=MATS_PROVIDED,
    ))

#### CANDY JAR GUESSES ####

C_COOKIE_JAR = ((7.5, 9), 0.5)
C_MALLOW_JAR = ((5, 7.5), 1 / 8)  # h=6.5, c=42

cprint(31, "\n\nCANDY GUESS TESTS -> (MIN, GUESS, MAX)")

cprint(32, "\nCOOKIE JAR")
cprint(
    36, "COOKIES;",
    candy_jar_guess(
        piece_dimensions=DIM_COOKIE,
        container_dimensions=C_COOKIE_JAR[0],
        container_offset=C_COOKIE_JAR[1],
    ))
cprint(
    36, "HERSHEY'S KISSES;",
    candy_jar_guess(
        piece_dimensions=DIM_KISS,
        container_dimensions=C_COOKIE_JAR[0],
        container_offset=C_COOKIE_JAR[1],
    ))
cprint(
    36, "REESE'S MINIS;",
    candy_jar_guess(
        piece_dimensions=DIM_RMINI,
        container_dimensions=C_COOKIE_JAR[0],
        container_offset=C_COOKIE_JAR[1],
    ))
cprint(
    36, "REESE'S CUPS;",
    candy_jar_guess(
        piece_dimensions=DIM_RCUP,
        container_dimensions=C_COOKIE_JAR[0],
        container_offset=C_COOKIE_JAR[1],
    ))
cprint(
    36, "OREOS;",
    candy_jar_guess(
        piece_dimensions=DIM_OREO,
        container_dimensions=C_COOKIE_JAR[0],
        container_offset=C_COOKIE_JAR[1],
    ))

cprint(32, "\nMALLOW JAR")
cprint(
    34, "MARSHMALLOWS (x42);",
    candy_jar_guess(
        piece_dimensions=DIM_MALLOW,
        container_dimensions=C_MALLOW_JAR[0],
        container_offset=C_MALLOW_JAR[1],
    ))
cprint(
    36, "OREOS;",
    candy_jar_guess(
        piece_dimensions=DIM_OREO,
        container_dimensions=C_MALLOW_JAR[0],
        container_offset=C_MALLOW_JAR[1],
    ))

cprint(32, "\nGRANDMA'S JAR")
cprint(
    34, "(h=4): REESE'S MINIS (x99);",
    candy_jar_guess(
        piece_dimensions=DIM_RMINI,
        container_dimensions=(7.5, 4),
        container_offset=1 / 8,
    ))
cprint(
    36, "MARSHMALLOWS;",
    candy_jar_guess(
        piece_dimensions=DIM_MALLOW,
        container_dimensions=(7.5, 9),
        container_offset=1 / 8,
    ))
