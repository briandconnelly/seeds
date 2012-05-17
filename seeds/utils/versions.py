# -*- coding: utf-8 -*-
"""
Collection of functions corresponding to SEEDS and plugin versions
"""

import operator

from seeds.SEEDSError import *

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


def is_valid_version(ver, target, op='='):
    '''Check to see if a version is valid

    Parameters:

    *ver*
        The version tuple to be checked
    *target*
        The version tuple to be checked against
    *op*
        The version comparison operator.  One of <, <=, =, >=, >
    '''

    # TODO: update this to verlib when that's included in python

    ops = {'<': operator.lt, '<=': operator.le, '=': operator.eq,
           '>': operator.gt, '>=': operator.ge}

    try:
        return ops[op](ver, target)
    except KeyError:
        raise VersionOperatorError("'{op}' is not a valid version operator".format(op=op))
