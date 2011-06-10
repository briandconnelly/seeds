# -*- coding: utf-8 -*-
"""This file defines several Exceptions which may be thrown by SEEDS."""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


class SEEDSError(Exception):
    """Base class for all Exceptions related to SEEDS"""
    pass

class PluginNotFoundError(SEEDSError):
    """Error to be raised when a Plugin (of any type) is not found

    Attributes:

    *plugin*
        The name of the plugin requested (string)
    """

    def __init__(self, plugin):
        self.plugin = plugin

    def __str__(self):
        return "Plugin '%s' not found" % (self.plugin)


class ActionNotFoundError(PluginNotFoundError):
    """Error to be raised when a Action Plugin is not found

    Attributes:

    *action*
        The name of the Action requested (string)
    """

    def __init__(self, action):
        self.action = action

    def __str__(self):
        return "Action type '%s' not found" % (self.action)


class CellNotFoundError(PluginNotFoundError):
    """Error to be raised when a Cell Plugin is not found

    Attributes:

    *cell*
        The name of the cell requested (string)
    """

    def __init__(self, cell):
        self.cell = cell

    def __str__(self):
        return "Cell type '%s' not found" % (self.cell)


class ResourceNotFoundError(PluginNotFoundError):
    """Error to be raised when a Resource Plugin is not found

    Attributes:

    *resource*
        The name of the Resource requested (string)
    """

    def __init__(self, resource):
        self.resource = resource

    def __str__(self):
        return "Resource type '%s' not found" % (self.resource)


class TopologyNotFoundError(PluginNotFoundError):
    """Error to be raised when a Topology Plugin is not found

    Attributes:

    *topology*
        The name of the Topology requested (string)
    """

    def __init__(self, topology):
        self.topology = topology

    def __str__(self):
        return "Topology type '%s' not found" % (self.topology)


class InvalidParameterValue(SEEDSError):
    """Error to be raised when a given parameter value is invalid

    Attributes:

    *section*
        The name of the section in which the parameter is defined
    *parameter*
        The name of the parameter
    """

    def __init__(self, section, parameter):
        self.section = section
        self.parameter = parameter

    def __str__(self):
        return "Invalid value for parameter '%s.%s'" % (self.section, self.parameter)

