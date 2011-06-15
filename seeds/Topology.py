# -*- coding: utf-8 -*-
"""
Interface for Topologies.

A topology is a graph that defines the interactions between nodes.  Each node
contains one Cell.  If a pair of nodes is connected, the Cells housed in those
nodes are thought of as "neighbors", and therefore can potentially interact
with each other.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly, Luis Zaman"

import random
import math

import networkx as nx


class Topology(object):
    """
    All topologies contain properties:

        graph
            A NetworkX graph object defining the connections between cells.
        experiment
            Reference to the Experiment in which it exists
        population
            A Reference to the Population object representing this population

    """

    def __init__(self, experiment, population):
        """Initialize a Topology object.

        The topology will have no cells and an empty graph

        Parameters:

        *experiment*
            A reference to the Experiment
        *population*
            A reference to the Population

        """

        self.experiment = experiment
        self.population = population
        self.graph = nx.Graph()

    def __str__(self):
        """Return a string to be used when a Topology object is printed"""
        return 'SEEDS Population Topology'

    def get_neighbors(self, node):
        """Get a list of neighboring cells for a given node

        Parameters:
        
        *node*
            The ID of the node whose neighboring cells to get
        
        """

        return [self.graph.node[n]['cell'] for n in self.graph.neighbors(node)]

    def size(self):
        """Get the number of nodes in the topology"""
        return len(self.graph)

    def update(self):
        """Update Cells in the Topology
        
        Update is asynchronous.  Nodes are chosen at random, and the Cell
        residing in those nodes is then updated.  The number of nodes to update
        per epoch is specified by the events_per_epoch parameter in the
        [Experiment] configuration block.  By default, the number of nodes to
        update is equal to the number of nodes in the Topology.
        
        """

        for x in xrange(self.experiment.config.getint(section='Experiment',
                                                 name='events_per_epoch',
                                                 default=len(self.graph))):
            node = random.choice(self.graph.nodes())
            self.graph.node[node]['cell'].update(self.get_neighbors(node))

    def teardown(self):
        """Perform any necessary cleanup at the end of the experiment"""
        pass

