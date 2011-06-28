# -*- coding: utf-8 -*-
"""
This file houses static functions that are of general use.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import random


def mean(data):
    """Calculate the mean of a list of numbers

    Parameters:

    *data*
        a list of numbers whose mean to calculate

    """

    return float(sum(data))/len(data)

def std(data):
    """Calculate the standard deviation of a list of numbers

    Parameters:

    *data*
        a list of numbers whose standard deviation to calculate

    """
    m = mean(data)
    sumsq = 0

    for d in data:
        sumsq += (d - m)**2

    return (sumsq / len(data))**(0.5)

def roulette_select(items=[], fitnesses=[]):
    """Perform a fitness-proportional selection using a roulette wheel

    Parameters:

    *items*
        A list of items from which to select
    *fitnesses*
        A list of fitnesses of the corresponding items.  Larger values
        represent larger fitnesses and larger probabilities of being selected.

    """

    if len(items) != len(fitnesses):
        print "Error: Must supply items TODO"
    elif len(items) < 1:
        print "Error: Must supply items to choose from TODO"

    total_fitness = float(sum(fitnesses))
    rel_fitnesses = [f/total_fitness for f in fitnesses]
    p = [sum(rel_fitnesses[:i+1]) for i in xrange(len(rel_fitnesses))]

    for i in xrange(len(items)):
        if random.random() < p[i]:
            return items[i]

def is_numeric(s):
    """Determine whether or not a given string is a float or integer"""

    try:
        float(s)
        return True
    except ValueError:
        return False

