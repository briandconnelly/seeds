# -*- coding: utf-8 -*-
"""
Collection of commonly-used functions that deal with geometry, such as
calculating distances.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.utils.numeric import is_numeric

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
    dist = -1

    if len(point1) != len(point2):
        print("Error: dimensions do not match")
        return
    elif len(point1) > 1:
        dist = 0

        for dim in range(len(point1)):
            if periodic:
                d = abs(point1[dim] - point2[dim])
                d_periodic = abs(1-d)
                dist += min(d, d_periodic)**p
            else:
                dist += (point1[dim] - point2[dim])**p

    elif is_numeric(point1) and is_numeric(point2):
        if periodic:
            d = abs(point1 - point2)
            d_periodic = abs(1-d)
            dist = min(d, d_periodic)**p
        else:
            dist = (point1 - point2)**p

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

def euclidean_distance_squared(p1, p2, periodic=False):
    """Calculate the squared Euclidean distance between two points.  This
    function is intended to be used in cases where the sqrt in Euclidean
    distance can be skipped in order to speed up calculations.

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

    return minkowski_distance_p(point1=p1, point2=p2, p=2, periodic=periodic)

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

