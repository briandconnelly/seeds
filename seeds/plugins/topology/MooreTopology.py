# -*- coding: utf-8 -*-
"""
Lattice topology in which each node is connected with each of its 8 neighbors
(Moore Neighborhood).  The radius of interactions can be defined, which means
all nodes within this many hops will be considered a neighbor.

This topology was originally presented and used used in the publication:

    B.D. Connelly, L. Zaman, C. Ofria, and P.K. McKinley, "Social structure and
    the maintenance of biodiversity," in Proceedings of the 12th International
    Conference on the Synthesis and Simulation of Living Systems (ALIFE), pp.
    461-468, 2010.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly, Luis Zaman, Philip McKinley, Charles Ofria"

from math import floor

import networkx as nx

from seeds.SEEDSError import *
from seeds.Topology import *


class MooreTopology(Topology):
    """
    Lattice topology with Moore Neighborhoods with configurable radius

    Nodes are organized on a lattice.  A node's neighbors reside to the
    left, right, above, below, and on the diagonals.  With radius 1, this
    neighborhood will contain 8 nodes.  With radius 2, the 24 nodes within
    a 2-hop distance are included.

    Configuration: All configuration options should be specified in the
        MooreTopology block (unless otherwise specified by the config_section
        parameter).

        size: Width/height, in number of nodes, of the Experiment.  With size
            10, there would be 100 nodes. (no default)
        periodic: Whether or not the Experiment should form a torus.
            This means that nodes on the left border are neighbors with
            nodes on the right border. (default: False)
        radius: Number of hops within a focal node's neighborhood
            (default: 1)

    Example:
        [MooreTopology]
        size = 100
        periodic = True
        radius = 4


    """
    def __init__(self, experiment, label=None):
        """Initialize a MooreTopology object"""
        super(MooreTopology, self).__init__(experiment, label=label)

        if self.label:
            self.config_section = "%s:%s" % ("MooreTopology", self.label)
        else:
            self.config_section = "%s" % ("MooreTopology")

        self.size = self.experiment.config.getint(self.config_section, 'size')
        self.periodic = self.experiment.config.getboolean(self.config_section, 'periodic', default=False)
        self.radius = self.experiment.config.getint(self.config_section, 'radius', default=1)
        self.dimensions = 2

        if not self.size:
            raise ConfigurationError("MooreTopology: size parameter must be defined")
        elif self.size < 1:
            raise ConfigurationError("MooreTopology: size must be positive")
        elif self.radius < 0:
            raise ConfigurationError("MooreTopology: radius must b greater than or equal to 0")
        elif self.radius >= self.size:
            raise ConfigurationError("MooreTopology: radius can not exceed grid size")

        self.graph = self.moore_2d_graph(self.size, self.size,
                                         radius=self.radius,
                                         periodic=self.periodic)

        for n in self.graph.nodes():
            self.graph.node[n]['coords'] = (self.row(n)/float(self.size), self.column(n)/float(self.size))

    def __str__(self):
        """Produce a string to be used when an object is printed"""
        return 'Moore Topology (%d nodes, %d radius)' % (self.size * self.size, self.radius)

    def row(self, nodeid):
        """Get the number of the row in which the given node is located

        Parameters:

        *nodeid*
            The ID of the node in question

        """
        return (nodeid//self.size)

    def column(self, nodeid):
        """Get the number of the column in which the given node is located

        Parameters:

        *nodeid*
            The ID of the node in question

        """
        return nodeid % self.size

    def node_id(self, row, col):
        """Get the ID of the node at the given row and column

        Parameters:

        *row*
            The row in which the node is located
        *col*
            The column in which the node is located

        """
        return row * self.size + col

    def moore_2d_graph(self, rows=0, columns=0, radius=0,
                       periodic=False):
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
            between a node and all other nodes within N hops)
        *periodic*
            Prevent edge effects using periodic boundaries

        """
        G = nx.empty_graph()
        G.name = "moore_2d_radius_graph"
        G.add_nodes_from(list(range(rows * columns)))

        for n in G.nodes():
            myrow = self.row(n)
            mycol = self.column(n)

            for r in range(myrow - radius, myrow + radius + 1):
                if periodic == False and (r < 0 or r >= rows):
                    continue

                for c in range(mycol - radius, mycol + radius + 1):
                    if periodic == False and (c < 0 or c >= columns):
                        continue

                    nid = self.node_id(r % rows, c % columns)

                    if nid != n:
                        neighbor_id = ((r % rows) * self.size) + (c % columns)
                        G.add_edge(n, neighbor_id)

        return G

    def add_node(self, id=-1, neighbors=[]):
        """Add a node to the graph.  Not supported by this topology type"""
        raise ConfigurationError("add_node is not supported by MooreTopology")
        return

    def remove_node(self, id):
        """Remove a node from the graph.  Not supported by this topology
        type"""
        raise ConfigurationError("remove_node is not supported by MooreTopology")
        return

    def add_edge(self, src, dest):
        """Add an edge to the graph.  Not supported by this topology type"""
        raise ConfigurationError("add_edge is not supported by MooreTopology")
        return

    def remove_edge(self, src, dest):
        """Remove an edge from the graph.  Not supported by this topology
        type"""
        raise ConfigurationError("remove_edge is not supported by MooreTopology")
        return


    def get_nearest_node(self, coords, n=1):
        """Return a list of the node(s) located nearest the given coordinates

        Note that this overwrites the get_nearest_node method defined by
        Topology (due to its simplicity vs using a k-d Tree).  This specific
        implementation may be removed in future releases if the more complete
        version in Topology is found to be better.

        Parameters:

        coords
            Tuple defining the point in question.  The number of dimensions
            should match the number of dimensions of the topology.
        n
            The number of nearest neighbors to find

        """

        if not coords or len(coords) < 1:
            print("ERROR: Invalid coordinates for get_nearest_node")
            return
        elif n < 1:
            print("ERROR: Invalid number of neighbors for get_nearest_node")
            return

        cell_width = 1.0 / self.size

        nearest_x = floor(float(coords[0]) / cell_width) * cell_width
        nearest_y = floor(float(coords[1]) / cell_width) * cell_width

        nearest_col = int(floor(coords[0] / cell_width))
        nearest_row = int(floor(coords[1] / cell_width))
        nearest_node = self.node_id(nearest_row, nearest_col)

        nearest = [nearest_node]

        for i in range(n - 1):
            print("ERROR: get_nearest_node only supports 1 neighbor at the moment")
            # TODO: look at neighbors of calculated nearest point and expand out.  Append to nearest.

        return nearest
