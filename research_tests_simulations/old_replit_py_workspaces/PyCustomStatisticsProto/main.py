from statistics import Data, IndepVar
from research_tests_simulations.old_replit_py_workspaces.PyCustomStatisticsProto.statistics.functions import mean

from research_tests_simulations.old_replit_py_workspaces.PyCustomStatisticsProto.sampling import samplingDist

pop = IndepVar([1, 2, 3, 4, 5, 6]).pow(2)
pop.title = "d6 * d6 * d6"

print(pop)

def testSampDist(rep: bool, rnd: int | None = 3) -> Data:
    N = 3
    d = samplingDist(
        population=pop.toList(),
        n=N,
        fx=mean,
        replacement=rep,
        rounded=rnd
    )
    d.title = (
        f"""Sampling Distribution of means [n={N},{
            ' no ' if not rep else ' '
        }replacement]"""
    )
    print(d.title)
    print(d.__get_summary__())
    print()
    return d


testSampDist(rep=True)
testSampDist(rep=False)

