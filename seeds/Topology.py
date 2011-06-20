# -*- coding: utf-8 -*-
"""
Interface for Topologies.

A topology is a graph that defines the interactions between nodes.  Each node
contains one Cell or one Resource.  If a pair of nodes is connected, the Cells
or Resources housed in those nodes are thought of as "neighbors", and therefore
can potentially interact with each other.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly, Luis Zaman"

import networkx as nx


class Topology(object):
    """
    All topologies contain properties:

        config_section
            The name of the section in the configuration file that stores the
            configuration for this Topology
        graph
            A NetworkX graph object defining the connections between cells.
        experiment
            Reference to the Experiment in which it exists

    """

    def __init__(self, experiment, config_section=None):
        """Initialize a Topology object.

        The topology will have no cells and an empty graph

        Parameters:

        *experiment*
            A reference to the Experiment
        *config_section*
            The name of the section in the configuration file that stores the
            configuration for this Topology

        """

        self.experiment = experiment
        self.graph = nx.Graph()
        self.config_section = config_section

    def __str__(self):
        """Return a string to be used when a Topology object is printed"""
        return 'SEEDS Topology'

    def get_neighbors(self, node):
        """Get a list of neighboring nodes (ids) for a given node

        Parameters:
        
        *node*
            The ID of the node whose neighboring cells to get
        
        """

        return self.graph.neighbors(node)

    def num_nodes(self):
        """Get the number of nodes in the topology"""
        return len(self.graph)

    def teardown(self):
        """Perform any necessary cleanup at the end of the experiment"""
        pass

