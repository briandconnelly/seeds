# -*- coding: utf-8 -*-
"""
Collection of functions that implement commonly-used selection algorithms, such
as roulette selection.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import random


def roulette_select(items=[], fitnesses=[], n=1):
    """Perform a fitness-proportional selection using a roulette wheel

    Parameters:

    *items*
        A list of items from which to select
    *fitnesses*
        A list of fitnesses of the corresponding items.  Larger values
        represent larger fitnesses and larger probabilities of being selected.
    *n*
        Number of items to select (default: 1)

    """

    if len(items) != len(fitnesses):
        print "Error: Must supply items TODO"
    elif len(items) < 1:
        print "Error: Must supply items to choose from TODO"

    total_fitness = float(sum(fitnesses))
    rel_fitnesses = [f/total_fitness for f in fitnesses]
    p = [sum(rel_fitnesses[:i+1]) for i in xrange(len(rel_fitnesses))]

    winners = []
    while len(winners) < n:
        for i in xrange(len(items)):
            if random.random() < p[i]:
                winners.append(items[i])
                break

    return winners
