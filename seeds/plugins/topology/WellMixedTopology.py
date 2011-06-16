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

    Example:
        [WellMixedTopology]
        size = 100000
        num_interactions = 10


    """
    def __init__(self, experiment, config_section='WellMixedTopology'):
        """Initialize a WellMixedTopology object"""
        super(WellMixedTopology, self).__init__(experiment, config_section=config_section)

        self.size = self.experiment.config.getint(section=self.config_section,
                                                  name='size')

        self.num_interactions = self.experiment.config.getint(section=self.config_section,
                                                              name='num_interactions',
                                                              default=self.size)

        if self.size < 1:
            print 'Error: Must specify the size of the population'

        self.graph = nx.empty_graph()
        self.graph.name = "well_mixed_graph"
        self.graph.add_nodes_from(range(self.size))

        for n in self.graph.nodes():
            self.graph.node[n]['coords'] = (random.random(),random.random())

    def __str__(self):
        """Produce a string to be used when an object is printed"""
        return 'Well-Mixed Topology (%d nodes, %d interactions)' % (self.size, self.num_interactions)


    def get_neighbors(self, node):
        """Get a randomly-selected list of neighboring nodes (IDs) for a given node

        Parameters:

        *node*
            The ID of the node whose neighboring nodes to get

        """

        return random.sample(self.graph.nodes(), self.num_interactions)

