# -*- coding: utf-8 -*-
""" Plugin defines the base properties and methods for SEEDS plugins. The
functionalities provided by Plugin allow plugin authors to describe their
plugins and any dependencies that their plugins may have and users to recreate
experiments exactly.

"""

# TODO: any special requirements options for NetworkX, numpy, scipy, and matplotlib?  They're likely to be common.
# TODO: build in unit tests??

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

class Plugin(object):
    """ Interface for Plugins

    Properties

    __name__:
        The name of the Plugin, e.g. "SmallWorldNetwork"
    __version__:
        The version of the Plugin. Plugin versions contain a major number and a
        minor number. These numbers are separated by a period (e.g., 2.13 is
        minor version 13 of major version 2).
    __author__:
        The name of the Plugin's primary author
    __credits__:
        Any additional credits
    __description__:
        A brief description of the Plugin
    __type__:
        The Plugin type.  One of 1=Cell, 2=Topology, 3=ResourceCell, 3=Action
    __requirements__:
        List of requirement Plugins that this Plugin may have.  Each item is a
        string of the form "<plugin>" or "<plugin> <operator> <version>".
        Operator is one of <, <=, =, >=, >.

    """

    __name__ = ""
    __version__ = 0.0
    __author__ = ""
    __credits__ = ""
    __description__ = ""
    __type__ = 0
    __requirements__ = []

    TYPE_UNSPECIFIED = 0
    TYPE_CELL = 1
    TYPE_TOPOLOGY = 2
    TYPE_RESOURCECELL = 3
    TYPE_ACTION = 4

    def __init__(self):
        """ Initialize the plugin """
        pass

    def update(self):
        """ Update the state of the plugin """
        pass

    def teardown(self):
        """ Perform any necessary cleanup at the end of the experiment """
        pass

    def version(self):
        return self.__version__

