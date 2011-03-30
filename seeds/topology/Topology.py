# -*- coding: utf-8 -*-
"""
Interface for Topologies.

A topology is a graph.  Each node contains a Cell and a ResourceManager.  If a
pair of nodes is connected, the Cells housed in those nodes are thought of as
"neighbors", and therefore can potentially interact with each other.

TODO: discuss reasoning for 1 cell per node.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.2"
__credits__ = "Brian Connelly, Luis Zaman"

import random
import math

import networkx as nx

from seeds.CellManager import *
from seeds.Resource import *
from seeds.ResourceManager import *

class Topology(object):
    """
    All topologies contain properties:

        world
            Reference to the World in which it exists
        id
            Unique ID
        cell_manager
            A CellManager object to create appropriate cells.
        typeCount
            List containing the number of cells currently existing for each
            Cell type.  Updated with increment_type_count(),
            decrement_type_count(), and update_type_count() methods.
        graph
            A NetworkX graph object defining the connections between cells.

    """

    def __init__(self, world, id):
        """Initialize a Topology object.

        The topology will have no cells and an empty graph

        Parameters:

        *world*
            A reference to the World
        *id*
            A unique ID for the created Topology

        """

        self.world = world
        self.id = id
        self.typeCount = []
        self.graph = nx.Graph()
        self.cell_manager = CellManager(self.world, self)

    def __str__(self):
        """Return a string to be used when a Topology object is printed"""
        return 'Topology %d' % (self.id)

    def increment_type_count(self, type):
        """Increment the cell type count for the given type

        Parameter:

        *type*
            The cell type whose count to increment

        """
        if len(self.typeCount) <= type:
            self.typeCount.extend([0] * (1 + type-len(self.typeCount)))
        self.typeCount[type] += 1

    def decrement_type_count(self, type):
        """Decrement the cell type count for the given type

        Parameter:

        *type*
            The cell type whose count to decrement

        """

        self.typeCount[type] -= 1

    def update_type_count(self, fromtype, totype):
        """Update the cell type counts, subtracting from the 'from' type and
        adding to the 'to' type

        Parameters:

        *fromtype*
            The type that a cell was prior to being updated
        *totype*
            The type that a cell is after being updated

        """

        self.decrement_type_count(fromtype)
        x = self.typeCount[totype]
        self.increment_type_count(totype)
        if x != self.typeCount[totype]-1:
            print "ERROR!"

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
        """Update Cells and Resources in the Topology
        
        Update is asynchronous.  Nodes are chosen at random, and the Cell and
        Resources residing in those nodes are then updated.  The number of
        nodes to update per epoch is specified by the events_per_epoch
        parameter in the [Experiment] configuration block.  By default, the
        number of nodes to update is equal to the number of nodes in the
        Topology.
        
        """

        for x in xrange(self.world.config.getint(section='Experiment',
                                                 name='events_per_epoch',
                                                 default=len(self.graph))):
            node = random.choice(self.graph.nodes())
            self.graph.node[node]['resource_manager'].update()
            self.graph.node[node]['cell'].update(self.get_neighbors(node))

