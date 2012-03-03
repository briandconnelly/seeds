# -*- coding: utf-8 -*-
"""
Collection of functions that perform different types of parsing
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import re

from seeds.SEEDSError import *


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

def parse_version_string(s):
    """Parse a version string and return a 3-element dict with keys 'operator',
    'major', and 'minor'. Input strings are of the form:

           <operator><major_version>.<minor_version>

    Where <operator> is one of: <, <=, =, >=, or >.  Although not recommended,
    when the operator is omitted, = will be used.

    """

    pattern = '^\s*(?P<operator>[<>=]+)\s*(?P<major>\d+)\.(?P<minor>\d+)\s*$'
    pattern = '^\s*(?P<operator>[<>=]+)?\s*(?P<major>\d+)\.(?P<minor>\d+)\s*$'
    match = re.match(pattern, s)
    if match:
        retval = {}

        if retval['operator'] == None:
            retval['operator'] = '='
        else:
            retval['operator'] = match.group('operator')

        retval['major'] = match.group('major')
        retval['minor'] = match.group('minor')
        return retval
    else:
        raise VersionStringFormatError(s)

