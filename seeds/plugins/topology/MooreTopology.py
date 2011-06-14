# -*- coding: utf-8 -*-
"""
Lattice topology in which each cell is connected with each of its 8 neighbors
(Moore Neighborhood).  The radius of interactions can be defined, which means
all cells within this many hops will be considered a neighbor.

This topology was originally presented and used used in the publication:

    B.D. Connelly, L. Zaman, C. Ofria, and P.K. McKinley, "Social structure and
    the maintenance of biodiversity," in Proceedings of the 12th International
    Conference on the Synthesis and Simulation of Living Systems (ALIFE), pp.
    461-468, 2010.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly, Luis Zaman, Philip McKinley, Charles Ofria"

import random
import math

from seeds.Resource import *
from seeds.ResourceManager import *
from seeds.Topology import *

import networkx as nx


class MooreTopology(Topology):
    """
    Lattice topology with Moore Neighborhoods with configurable radius

    Cells are organized on a lattice.  A cell's neighbors reside to the
    left, right, above, below, and on the diagonals.  With radius 1, this
    neighborhood will contain 8 cells.  With radius 2, the 24 cells within
    a 2-hop distance are included.

    Configuration: All configuration options should be specified in the
        MooreTopology block.

        size: Width/height, in number of cells, of the Experiment.  With size
            10, there would be 100 cells. (no default)
        periodic_boundaries: Whether or not the Experiment should form a torus.
            This means that cells on the left border are neighbors with
            cells on the right border. (default: False)
        radius: Number of hops within a focal cell's neighborhood
            (default: 1)

    Example:
        [MooreTopology]
        size = 100
        periodic_boundaries = True
        radius = 4


    """
    def __init__(self, experiment, population, id):
        """Initialize a MooreTopology object"""
        super(MooreTopology, self).__init__(experiment, population, id)

        self.size = self.experiment.config.getint('MooreTopology', 'size')
        self.periodic_boundaries = self.experiment.config.getboolean('MooreTopology', 'periodic_boundaries', default=False)
        self.radius = self.experiment.config.getint('MooreTopology', 'radius', default=1)

        if self.radius >= self.size:
            print 'Error: Radius cannot be bigger than experiment!'

        self.graph = self.moore_2d_graph(self.size, self.size,
                                         radius=self.radius,
                                         periodic_boundaries=self.periodic_boundaries)

        for n in self.graph.nodes():
            self.graph.node[n]['cell'] = self.experiment.create_cell(population=self.population, node=self.graph.node[n], id=n)
            self.graph.node[n]['cell'].coords = (self.row(n), self.column(n))
            self.graph.node[n]['resource_manager'] = ResourceManager(experiment, self)

    def __str__(self):
        """Produce a string to be used when an object is printed"""
        return 'Moore Topology (%d cells, %d radius)' % (self.size * self.size, self.radius)

    def row(self, cellid):
        """Get the number of the row in which the given cell is located

        Parameters:

        *cellid*
            The ID of the cell in question

        """
        return (cellid/self.size)

    def column(self, cellid):
        """Get the number of the column in which the given cell is located

        Parameters:

        *cellid*
            The ID of the cell in question

        """
        return cellid % self.size

    def cell_id(self, row, col):
        """Get the ID of the cell at the given row and column

        Parameters:

        *row*
            The row in which the cell is located
        *col*
            The column in which the cell is located

        """
        return row * self.size + col

    def moore_2d_graph(self, rows=0, columns=0, radius=0,
                       periodic_boundaries=False):
        """ Return the 2d grid graph of rows x columns nodes,
            each connected to its nearest Moore neighbors within
            a given radius.
            Optional argument periodic=True will connect
            boundary nodes via periodic boundary conditions.

        Parameters:

        *rows*
            The number of rows to be in the graph
        *columns*
            The number of columns to be in the graph
        *radius*
            The radius of interactions in the graph (there will be an edge
            between a cell and all other cells within N hops)
        *periodic_boundaries*
            Prevent edge effects using periodic boundaries

        """
        G = nx.empty_graph()
        G.name = "moore_2d_radius_graph"
        G.add_nodes_from(range(rows * columns))

        for n in G.nodes():
            myrow = self.row(n)
            mycol = self.column(n)

            for r in xrange(myrow - radius, myrow + radius + 1):
                if periodic_boundaries == False and (r < 0 or r >= rows):
                    continue

                for c in xrange(mycol - radius, mycol + radius + 1):
                    if periodic_boundaries == False and (c < 0 or c >= columns):
                        continue

                    cid = self.cell_id(r % rows, c % columns)

                    if cid != n:
                        neighbor_id = ((r % rows) * self.size) + (c % columns)
                        G.add_edge(n, neighbor_id)

        return G

