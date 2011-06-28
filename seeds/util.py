# -*- coding: utf-8 -*-
"""
This file houses static functions that are of general use.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from math import sqrt
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


def square_distance(p1, p2, periodic=False):
    """Calculate the square distance between two points.

    Arguments:

    *p1*
        A tuple containing the coordinates of the first point
    *p2*
        A tuple containing the coordinates of the second point
    *periodic*
        Whether or not periodic boundaries are used.  If they are, the distance
        along any dimension is the minimum of the distance between the two
        points not using the periodic edges or the distance using those edges.

    """

# TODO: problem.  if dimensions is 1, it is an integer, which has no length

    if len(p1) != len(p2):
        print "Error: dimensions do not match"
        return
    elif len(p1) == 1:
        d = abs(p1-p2)

        if periodic:
            return min(d, abs(1-d))**2
        else:
            return d**2
    else:
        dist = 0

        for dim in xrange(len(p1)):
            if periodic:
                d = abs(p1[dim] - p2[dim])
                d_periodic = abs(1-d)
                dist += min(d, d_periodic)**2
            else:
                dist += (p1[dim] - p2[dim])**2

        return dist

def euclidean_distance(p1, p2, periodic=False):
    """Calculate the Euclidean distance between two points.

    Arguments:

    *p1*
        A tuple containing the coordinates of the first point
    *p2*
        A tuple containing the coordinates of the second point
    *periodic*
        Whether or not periodic boundaries are used.  If they are, the distance
        along any dimension is the minimum of the distance between the two
        points not using the periodic edges or the distance using those edges.

    """

    return sqrt(square_distance(p1, p2, periodic))

