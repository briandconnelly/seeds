# -*- coding: utf-8 -*-
"""This file defines several Exceptions which may be thrown by SEEDS."""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


class SEEDSError(Exception):
    """Base class for all Exceptions related to SEEDS"""
    pass

class ResourceNotDefinedError(SEEDSError):
    """Error to be raised when a Resource is requested that has not been
    defined.

    Attributes:

    *resource*
        The name of the requested Resource (string)

    """

    def __init__(self, resource):
        self.resource = resource

    def __str__(self):
        return "Resource '%s' not defined" % (self.resource)


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


class ActionPluginNotFoundError(PluginNotFoundError):
    """Error to be raised when a Action Plugin is not found

    Attributes:

    *action*
        The name of the Action requested (string)
    """

    def __init__(self, action):
        self.action = action

    def __str__(self):
        return "Action '%s' not found" % (self.action)


class CellPluginNotFoundError(PluginNotFoundError):
    """Error to be raised when a Cell Plugin is not found

    Attributes:

    *cell*
        The name of the cell requested (string)
    """

    def __init__(self, cell):
        self.cell = cell

    def __str__(self):
        return "Cell plugin '%s' not found" % (self.cell)

class CellTypeError(SEEDSError):
    """Error to be raised when an invalid Cell type is used

    Attributes:

    *celltype*
        The attempted cell type ID
    """

    def __init__(self, celltype):
        self.celltype = celltype

    def __str__(self):
        return "Cell type '%s' not found" % (self.celltype)


class ResourceCellPluginNotFoundError(PluginNotFoundError):
    """Error to be raised when a ResourceCell Plugin is not found

    Attributes:

    *resource*
        The name of the ResourceCell requested (string)
    """

    def __init__(self, resource):
        self.resource = resource

    def __str__(self):
        return "ResourceCell '%s' not found" % (self.resource)


class TopologyPluginNotFoundError(PluginNotFoundError):
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

class NonExistentNodeError(SEEDSError):
    """Error to be raised when a node does not exist

    Attributes:

    *id*
        The ID of the node
    """

    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "Node %d does not exist in Topology" % (self.id)

class NonExistentEdgeError(SEEDSError):
    """Error to be raised when an edge does not exist

    Attributes:

    *src*
        The ID of the first node connected with the edge
    *dest*
        The ID of the second node connected with the edge
    """

    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def __str__(self):
        return "Edge %d-%d does not exist in Topology" % (self.src, self.dest)

class ConfigurationError(SEEDSError):
    """Error to be raised when an invalid configuration is given, either
    through one bad parameter value or through parameter value conflicts.

    Attributes:

    *message*
        The message to be displayed (string)

    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
