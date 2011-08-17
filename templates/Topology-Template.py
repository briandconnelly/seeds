# -*- coding: utf-8 -*-

""" This template outlines the necessary components for implementing a new
Topology in SEEDS.  Topologies are used in SEEDS to model the interactions
between organisms and the flow of resources through space.  These are modeled
as graphs, which a Topology creates and maintains.  These graphs could be
simple lattices (as used by SEEDS' included MooreTopology and
VonNeumannTopology) or more complex structures.

Areas marked with 'TODO' should be replaced with code specific to the Topology
being implemented.

Generally, creating a new Topology requires creating a new constructor
(__init__), building a graph using NetworkX, and implementing methods to add
and remove nodes and edges.

The name of the Topology type should be the name of the class.  The name of the
file should also match this.

Methods and parameters common to all Topology objects can be seen in the
Topology.py file in the main SEEDS codebase.

Once completed, new Topology type files can be placed in a plugins directory
and used by specifying the name of the file/class with the "topology" parameter
in the [Population] or a [Resource]  section of the configuration file.

"""

__author__ = "TODO"
__credits__ = "TODO"


import networkx as nx
import random

from seeds.SEEDSError import *
from seeds.Topology import *


class TODO-TopologyName(Topology):
    """ TODO: documentation about this Topology type including the motivation
    behind it, any parameters that can be defined in configuration files, and
    other pertinent information.
    """

    # TODO: the __init__ method (or "constructor") is called when a new
    # Topology object is created.  Generally, a constructor will read parameter
    # values from a config file, validate those values, and build the graph.

    def __init__(self, experiment, config_section='TODO-TopologyName'):
        """Initialize a TODO-TopologyName object"""
        super(TODO-TopologyName, self).__init__(experiment, config_section=config_section)

        # TODO: here is a good place to get parameter values from the configuration file
        self.size = self.experiment.config.getint(self.config_section, 'size')

        # TODO: define the number of dimensions for this space.  It can be
        # configurable or fixed.
        self.dimensions = self.experiment.config.getinit(self.config_section, 'dimensions', default=2)

        # TODO: the constructor is a good place to make sure configured values are valid
        if self.size < 1:
            raise ConfigurationError("TODO-TopologyName: size must be positive")


        # TODO: create the graph.  SEEDS uses NetworkX for graph functionality,
        # so a number of predefined graph types can be used, or new ones can be
        # created by adding nodes and edges accordingly.  See
        # http://networkx.lanl.gov/.

        self.graph = TODO

        # TODO: it is also good to assign coordinates to each node in the
        # graph.  This tuple is placed in the ['coords'] attribute of each
        # node.  Here, we assign each node a random 2-dimensional location.
        for n in self.graph.nodes():
            self.graph.node[n]['coords'] = tuple([random.random() for i in xrange(self.dimensions)])


    # TODO: the __str__ method returns a string to be used when an object is
    # printed.  This can be a useful place to return information that is
    # specific to the Topology type
    def __str__(self):
        """Produce a string to be used when an object is printed"""
        return 'TODO-TopologyName Topology (%d nodes)' % (self.size)


    # TODO: the following methods allow the underlying graph to be altered
    # through the addition and removal of nodes and edges.  The basic Topology
    # class provides these functions on its own, so if you wish to use them,
    # these methods can be removed from this file.  However, if you wish to use
    # a static graph, these methods should be overrided as below to prevent the
    # graph from being modified.
    
    # Below, instead of modifying the graph whenever these methods are called,
    # nothing is done.  In these cases, it is useful to either throw a
    # ConfigurationError or print an error message indicating that these
    # operations are not supported when these methods are called.

    def add_node(self, id=-1, neighbors=[]):
        """Add a node to the graph."""
        return

    def remove_node(self, id):
        """Remove a node from the graph."""
        return

    def add_edge(self, src, dest):
        """Add an edge to the graph."""
        return

    def remove_edge(self, src, dest):
        """Remove an edge from the graph."""
        return

