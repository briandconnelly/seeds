# -*- coding: utf-8 -*-
"""
Collection of functions that perform different types of parsing
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import re


def parse_int_rangelist(s, sorted=False):
    """Parse a list of numeric ranges.  These lists are a comma-separated list
    of either single numbers or ranges, specified by number-number.

    Parameters:

    s
        A string containing a comma-separated list of integers and ranges of
        integers
    sorted
        Whether or not to sort the resulting list (default: False)

    """

    range_pattern = "\s*(\-?\d+)\s*\-\s*(\-?\d+)\s*"

    retval = []

    if s:
        tokens = s.split(",")
        for t in tokens:
            match = re.match(range_pattern, t)
            if match:
                start = int(match.group(1))
                end = int(match.group(2))
                for i in range(start, end+1):
                    retval.append(i)
            else:
                try:
                    x = int(t)
                    retval.append(x)
                except ValueError:
                    print("Error: Can not parse token '%s' from range list '%s'" % (t, s))

    if sorted:
        retval.sort()

    return retval
