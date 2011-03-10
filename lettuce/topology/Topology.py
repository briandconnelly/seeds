"""
Interface for Topologies.

A Topology is a collection of Cell objects and a graph representing the
connections between these cells.  If a pair of Cell objects is connected, those
cells are thought of as "neighbors", and therefore interact with each other.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "0.9.0"
__credits__ = "Brian Connelly, Luis Zaman"

import random
import math

import networkx as nx

from lettuce.CellManager import *

class Topology(object):
    """
    All topologies contain properties:

        world - Reference to the World in which it exists
        id - Unique ID
        cells - List of Cell objects
        typeCount - Hash containing the number of cells currently
          existing for each Cell type.  Updated with increment_type_count(),
          decrement_type_count(), and update_type_count() methods.
        graph - A NetworkX graph object defining the connections between
          cells.

    NOTE: In future versions, Cell objects will be stored within the graph nodes,
      so the cells list will be removed.

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
        self.cells = []
        self.typeCount = []
        self.graph = nx.Graph()

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

    def get_neighbors(self, cell):
        """Get a list of neighbors for a given cell"""
        pass

    def size(self):
        """Get the number of cells in the topology"""
        return len(cells)

    def update(self):
        """Update all cells in the topology"""
        for x in xrange(self.world.config.getint(section='Experiment', name='events_per_epoch', default=len(self.cells))):
            cell = random.choice(self.cells)
            cell.update(self.get_neighbors(cell))

