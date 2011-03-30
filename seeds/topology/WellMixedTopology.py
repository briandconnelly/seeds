# -*- coding: utf-8 -*-
"""
Well-mixed topology in which each Cell is a neighbor of every other Cell.

This topology is modeled as a graph with no edges between the nodes.  Although
a complete graph would perhaps model a well-mixed topology more accurately,
this would prohibit large populations due to the associated memory
requirements.

Cells are given a randomly-assigned location to more easily allow for
visualization.  It should be noted that in this topology, interactions
are not localized, so the neighbors with which a cell interacts will
be located throughout the environment.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.1"
__credits__ = "Brian Connelly"

import random
import math

from seeds.CellManager import *
from seeds.topology.Topology import *
from seeds.Resource import *
from seeds.ResourceManager import *

import networkx as nx

class WellMixedTopology(Topology):
    """
    Well-mixed topology with a configurable number of interactions

    Configuration: All configuration options should be specified in the
        WellMixedTopology block.

        size
            Total number of cells in the population
        num_interactions
            When a Cell is updated, a list of neighbors is passed to it.
            This parameter specifies the size of a random subset of cells
            to be used as this neighbor set.  By default, all cells in
            the populaion are passed as neighbors.

    Example:
        [WellMixedTopology]
        size = 100000
        num_interactions = 10


    """
    def __init__(self, world, id):
        """Initialize a WellMixedTopology object"""
        Topology.__init__(self, world, id)

        self.size = self.world.config.getint(section='WellMixedTopology',
                                             name='size')

        self.num_interactions = self.world.config.getint(section='WellMixedTopology',
                                                         name='num_interactions',
                                                         default=self.size)

        if self.size < 1:
            print 'Error: Must specify the size of the population'

        self.graph = nx.empty_graph()
        self.graph.name = "well_mixed_graph"
        self.graph.add_nodes_from(range(self.size))

        for n in self.graph.nodes():
            self.graph.node[n]['cell'] = self.cell_manager.newcell(n, n)
            self.graph.node[n]['cell'].coords = (random.random(),random.random())
            self.graph.node[n]['resource_manager'] = ResourceManager(world, self)

    def __str__(self):
        """Produce a string to be used when an object is printed"""
        return 'Well-Mixed Topology (%d cells, %d interactions)' % (self.size, self.num_interactions)


    def get_neighbors(self, node):
        """Get a randomly-selected list of neighboring cells for a given node

        Parameters:

        *node*
            The ID of the node whose neighboring cells to get

        """
        neighbors = random.sample(self.graph.nodes(), self.num_interactions)
        return [self.graph.node[n]['cell'] for n in neighbors]

