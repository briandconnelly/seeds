# -*- coding: utf-8 -*-
""" Plugin defines the base properties and methods for SEEDS plugins. The
functionalities provided by Plugin allow plugin authors to describe their
plugins and any dependencies that their plugins may have and users to recreate
experiments exactly.

"""

# TODO: any special requirements options for NetworkX, numpy, scipy, and matplotlib?  They're likely to be common.
# TODO: build in unit tests??

__author__ = "Brian Connelly <bdc@bconnelly.net>"
__credits__ = "Brian Connelly"


class Plugin(object):
    """ Interface for Plugins

    Properties

    __name__:
        The class name of the Plugin, e.g. "SmallWorldNetwork"
    __description__:
        A brief description of the Plugin
    __version__:
        The version of the Plugin. Plugin versions are a tuple consisting of a
        major number and a minor number.  For example (2,13) is minor version
        13 of major version 2. When doing comparisons, Python handles tuples
        nicely, so if you want to test if a version is at least (2,7)
        "__version__ >= (2,7)".
    __author__:
        The name of the Plugin's primary author
    __credits__:
        Any additional credits
    __type__:
        The Plugin type.  One of 1=Cell, 2=Topology, 3=ResourceCell, 3=Action.
    __requirements__:
        List of requirement Plugins that this Plugin may have.  Each item is a
        string of the form "<plugin>" or "<plugin> <operator> <version>".
        Operator is one of <, <=, =, >=, >.

    """

    __name__ = ""
    __version__ = ()
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
        """Return the version of the Plugin"""
        return self.__version__

    def cmp_version(self, ver):
        """Compare this version of the plugin versus a given version returning
        -1 if the version of the plugin is less than the given version, 0 if
        they are equal, and 1 if it is greater.

        Parameters:

        *ver*
            A tuple containing the version to compare with

        """

        if self.__version__ < ver:
            return -1
        elif self.__version__ == ver:
            return 0
        elif self.__version__ > ver:
            return 1
