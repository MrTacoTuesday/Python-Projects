from research_tests_simulations.old_replit_py_workspaces.PyCustomStatisticsProto.statistics.Data import Data
from typing import List

from research_tests_simulations.old_replit_py_workspaces.PyCustomStatisticsProto.utility import Number, NumList, Samples, StatFunc


def allSamples(population: NumList,
               n: int,
               replacement: bool = False,
               __sample_ids: List[int] = []) -> Samples:
    """
    Return all possible samples of size n from population.
    :param population: list of values
    :param n: sample size
    :param replacement: if True, the samples are drawn with replacement, otherwise they are drawn without replacement
    :param __sample_ids: starting individual ids for the sample, for internal use only
    :return: list of all possible samples

    WARNING: Performance completion time increases greatly as the population size and sample size increases.
    """
    samples: Samples = []
    #print(f"[n={n}]\nCurrent Sample IDs: {__sample_ids}")
    for indivID in range(len(population)):
        if indivID in __sample_ids and not replacement:
            continue
        #print(f"Id: {indivID} Item: {population[indivID]}")
        if n == 1:
            __samp = [population[id] for id in [*__sample_ids, indivID]]
            #input(f"\tFinished Sample: {__samp}")
            samples.append(__samp)
        else:
            samples.extend(
                allSamples(population, n - 1, replacement,
                           __sample_ids + [indivID]))
            #print(f"[n={n}]")
    return samples


def samplingDist(population: NumList,
                 n: int,
                 fx: StatFunc,
                 replacement: bool,
                 rounded: int | None = None) -> Data:
    """
    Sampling distribution function.
    :param population: list of values
    :param n: sample size
    :param fx: function to obtain the sample statistic
    :param replacement: if True, the samples are drawn with replacement, otherwise they are drawn without replacement
    :param rounded: decimal places to round the sample statistics to
    :return: sample statistics data

    WARNING: Performance completion time increases greatly as the population size and sample size increases.
    """

    if len(population) < n and not replacement:
        raise ValueError(
            "The sample size is too big!! Allow replacement or increase the population data."
        )

    def _apply(x: NumList) -> Number:
        return fx(x) if rounded is None else round(fx(x), rounded)

    def all_samp_fs(n: int, __sample_ids: List[int] = []) -> NumList:
        samples: NumList = []
        for indivID in range(len(population)):
            if indivID in __sample_ids and not replacement:
                continue
            if n == 1:
                __samp = _apply(
                    [population[id] for id in [*__sample_ids, indivID]])
                samples.append(__samp)
            else:
                samples.extend(all_samp_fs(n - 1, __sample_ids + [indivID]))
        return samples

    return Data(all_samp_fs(n))
