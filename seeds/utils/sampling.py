# -*- coding: utf-8 -*-
"""
Collection of functions that implement commonly-used sampling/selection
algorithms, such as roulette selection.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import itertools
import random


def roulette_select(items=[], fitnesses=[], k=1):
    """Perform a fitness-proportional selection using a roulette wheel

    Parameters:

    *items*
        A list of items from which to select
    *fitnesses*
        A list of fitnesses of the corresponding items.  Larger values
        represent larger fitnesses and larger probabilities of being selected.
        Additionally, non-negative values are assumed.  Data that do not
        conform to these rules should be transformed before being passed to
        this function.
    *k*
        Number of items to select (default: 1)

    """

    if len(items) != len(fitnesses):
        print("Error: Must supply items")
    elif len(items) < 1:
        print("Error: Must supply items to choose from")

    total_fitness = float(sum(fitnesses))
    rel_fitnesses = [f/total_fitness for f in fitnesses]
    p = [sum(rel_fitnesses[:i+1]) for i in range(len(rel_fitnesses))]

    winners = []
    while len(winners) < k:
        for i in range(len(items)):
            if random.random() < p[i]:
                winners.append(items[i])
                break

    return winners

def sample_with_replacement(items=[], k=1):
    """Get a list of samples from a given set of items with replacement.

    Parameters:

    *items*
        A list of items from which to select
    *k*
        Number of items to select (default: 1)

    """

    samples = []
    popsize = len(items)

    if popsize < 1:
        print("Error: Must supply items")

    if k < 1:
        print("Error: Invalid number of samples")

    _random, _int = random.random, int
    return [items[_int(_random() * popsize)] for i in itertools.repeat(None, k)]

def sample_without_replacement(items=[], k=1):
    """Get a list of samples from a given set of items without replacement.

    This function is merely a wrapper for Python's random.sample()

    Parameters:

    *items*
        A list of items from which to select
    *k*
        Number of items to select (default: 1)

    """

    return random.sample(items, k)
