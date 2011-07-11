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
    except TypeError:
        return False

def minkowski_distance_p(point1, point2, p=2, periodic=False):
    """Calculate the Minkowski distance to the pth power between two points.

    This is the Minkowski distance calculation without the root.

    Arguments:

    *point1*
        A tuple containing the coordinates of the first point
    *point2*
        A tuple containing the coordinates of the second point
    *p*
        Order parameter.  A value of 2 yields Euclidean distance, while a value
        of 1 yields Manhattan distance.  (Default: 2)
    *periodic*
        Whether or not periodic boundaries are used.  If they are, the distance
        along any dimension is the minimum of the distance between the two
        points not using the periodic edges or the distance using those edges.

    """

    if len(point1) != len(point2):
        print "Error: dimensions do not match"
        return
    elif is_numeric(point1) and is_numeric(point2):
        if periodic:
            d = abs(point1 - point2)
            d_periodic = abs(1-d)
            dist = min(d, d_periodic)**p
        else:
            dist = (point1 - point2)**p

        return dist
    else:
        dist = 0

        for dim in xrange(len(point1)):
            if periodic:
                d = abs(point1[dim] - point2[dim])
                d_periodic = abs(1-d)
                dist += min(d, d_periodic)**p
            else:
                dist += (point1[dim] - point2[dim])**p

        return dist

def minkowski_distance(point1, point2, p=2, periodic=False):
    """Calculate the Minkowski distance between two points.

    Arguments:

    *point1*
        A tuple containing the coordinates of the first point
    *point2*
        A tuple containing the coordinates of the second point
    *p*
        Order parameter.  A value of 2 yields Euclidean distance, while a value
        of 1 yields Manhattan distance.  (Default: 2)
    *periodic*
        Whether or not periodic boundaries are used.  If they are, the distance
        along any dimension is the minimum of the distance between the two
        points not using the periodic edges or the distance using those edges.

    """

    return minkowski_distance_p(point1, point2, p=p, periodic=periodic)**(1.0/p)

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

    return minkowski_distance(point1=p1, point2=p2, p=2, periodic=periodic)

def manhattan_distance(p1, p2, periodic=False):
    """Calculate the Manhattan distance between two points.

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

    return minkowski_distance(point1=p1, point2=p2, p=1, periodic=periodic)

