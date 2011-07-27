# -*- coding: utf-8 -*-
"""
Collection of functions that implement commonly-used numeric algorithms
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


def is_numeric(s):
    """Test whether or not a given value is numeric (integer or float)"""

    try:
        float(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False
