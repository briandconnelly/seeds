# -*- coding: utf-8 -*-
"""
Well-mixed topology in which each node is a neighbor of every other node.

This topology is modeled as a graph with no edges between the nodes.  Although
a complete graph would perhaps model a well-mixed topology more accurately,
this would prohibit large populations due to the associated memory
requirements.

Nodes are given a randomly-assigned location to more easily allow for
visualization.  It should be noted that in this topology, interactions
are not localized, so the neighbors with which a node interacts will
be located throughout the environment.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import random
import networkx as nx

from seeds.SEEDSError import *
from seeds.Topology import *


class WellMixedTopology(Topology):
    """
    Well-mixed topology with a configurable number of interactions

    Configuration: All configuration options should be specified in the
        WellMixedTopology block (unless otherwise specified by the
        config_section parameter).

        size
            Total number of nodes in the population
        num_interactions
            When a node is updated, a list of neighbors is passed to it.
            This parameter specifies the size of a random subset of nodes
            to be used as this neighbor set.  By default, all nodes in
            the populaion are passed as neighbors.
        dimensions
            The number of dimensions in space that this topology occupies.
            (default: 2)

    Example:
        [WellMixedTopology]
        size = 100000
        num_interactions = 10


    """

    def __init__(self, experiment, label=None):
        """Initialize a WellMixedTopology object

        Parameters:

        *experiment*
            A reference to the Experiment
        *label*
            A unique string identifying the configuration for this topology

        """

        super(WellMixedTopology, self).__init__(experiment, label=label)

        if self.label:
            self.config_section="%s:%s" % ("WellMixedTopology", label)
        else:
            self.config_section="%s" % ("WellMixedTopology")

        self.size = self.experiment.config.getint(section=self.config_section,
                                                  name='size')
        self.num_interactions = self.experiment.config.getint(section=self.config_section,
                                                              name='num_interactions',
                                                              default=self.size)
        self.dimensions = self.experiment.config.getint(section=self.config_section,
                                                        name="dimensions",
                                                        default=2)
        if not self.size:
            raise ConfigurationError("WellMixedTopology: size must be defined")
        elif self.size < 1:
            raise ConfigurationError("WellMixedTopology: size must be greater than 0")
        elif self.num_interactions < 0:
            raise ConfigurationError("WellMixedTopology: num_interactions must be non-negative")
        elif self.num_interactions > self.size:
            raise ConfigurationError("WellMixedTopology: num_interactions can not exceed size")
        elif self.dimensions < 1:
            raise ConfigurationError("GrowthTopology: Number of dimensions must be at least 1")

        self.graph = nx.empty_graph()
        self.graph.name = "well_mixed_graph"
        self.graph.add_nodes_from(list(range(self.size)))

        for n in self.graph.nodes():
            self.graph.node[n]['coords'] = tuple([random.random() for i in xrange(self.dimensions)])

    def __str__(self):
        """Produce a string to be used when an object is printed"""
        return "Well-Mixed Topology (%d nodes, %d interactions)" % (self.size, self.num_interactions)

    def get_neighbors(self, node):
        """Get a randomly-selected list of neighboring nodes (IDs) for a given node

        Parameters:

        *node*
            The ID of the node whose neighboring nodes to get

        """

        return random.sample(self.graph.nodes(), self.num_interactions)

    def add_edge(self, src, dest):
        """Add an edge to the graph.  Not supported by this topology type"""
        raise ConfigurationError("add_edge is not supported by WellMixedTopology")
        return

    def remove_edge(self, src, dest):
        """Remove an edge from the graph.  Not supported by this topology
        type"""
        raise ConfigurationError("remove_edge is not supported by WellMixedTopology")
        return

    def add_node(self, id=-1, neighbors=[]):
        """Add a node to the graph.  Topologies that do not wish to support
        this should redefine this method to do nothing.  This method will
        not place a Cell or ResourceCell in the newly-created node.  That
        will need to be done separately.

        Note that since edges aren't used in this topology, the neighbors
        argument is ignored.

        Parameters:

        id
            The ID to use for the new node.  If none is specified (or -1), the
            ID used will be the current largest ID in the graph plus 1.
        neighbors
            An optional list of node IDs that will be connected to the new node
            via an edge. NonExistentNodeError will be raised if any of these
            nodes do not exist. ***This argument is ignored***

        """

        if id == -1:
            self.graph.add_node(max(self.graph.nodes()) + 1)
        else:
            self.graph.add_node(id)

        self.graph.node[id]['coords'] = (random.random(),random.random())

