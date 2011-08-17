# -*- coding: utf-8 -*-
"""
Topology in which the location of each node is represented by points randomly
placed on a 2D plane.  Each node is connected to a configured expected number
of neighbors.

This topology was originally presented and used used in the publication:

    B.D. Connelly, L. Zaman, C. Ofria, and P.K. McKinley, "Social structure and
    the maintenance of biodiversity," in Proceedings of the 12th International
    Conference on the Synthesis and Simulation of Living Systems (ALIFE), pp.
    461-468, 2010.

"""

__author__ = "Luis Zaman <zamanlui@msu.edu>"
__credits__ = "Luis Zaman, Brian Connelly, Philip McKinley, Charles Ofria"

import networkx as nx
import random
from math import sqrt, floor, ceil, pi

from seeds.SEEDSError import *
from seeds.Topology import *
from seeds.utils.geometry import euclidean_distance


class CartesianTopology(Topology):
    """
    Topology based on points in Cartesian space on a 2D plane

    Points are placed randomly on a unit two-dimensional Cartesian plane.
    Each node is connected to those nodes that fall within a given distance.
    This distance is calculated to yield an expected number of neighbors
    equal to the expected_neighbors configuration parameter.

    Configuration: All configuration parameters are specified in a
      [CartesianTopology<:label>] block.

    size
        Total number of nodes in the topology.  If size=1, the
        expected_neighbors parameter is ignored, since the one node can not
        have any neighbors. (Integer)
    periodic
        Whether or not to use periodic boundary conditions, which connects the
        edges of the plane, forming a torus. (Boolean.  Default: False)
    expected_neighbors
        The number of neighbors (expected) each node will have. (Default: 0)
    remove_disconnected
        Whether or not to remove nodes that do not have neighbors within the
        calculated radius.  If False, node is connected to a randomly-chosen
        neighbor (Boolean.  Default: True)
    config_section
        The name of the section in which this topology is configured

    Example:

    [CartesianTopology]
    size = 100000
    periodic = True
    expected_neighbors = 20

    """

    def __init__(self, experiment, label=None):
        """Initialize a CartesianTopology object

        Parameters:

        *experiment*
            A reference to the Experiment
        *label*
            A unique string identifying the configuration for this topology

        """

        super(CartesianTopology, self).__init__(experiment, label=label)

        if self.label:
            self.config_section="%s:%s" % ("CartesianTopology", label)
        else:
            self.config_section="%s" % ("CartesianTopology")

        self.size = self.experiment.config.getint(self.config_section, 'size')
        self.periodic = self.experiment.config.getboolean(self.config_section, 'periodic', default=False)
        self.expected_neighbors = self.experiment.config.getint(self.config_section, 'expected_neighbors', default=0)
        self.remove_disconnected = self.experiment.config.getboolean(self.config_section, 'remove_disconnected', default=True)
        self.dimensions = 2

        if not self.size:
            raise ConfigurationError("CartesianTopology: must specify a size")
        elif self.size < 1:
            raise ConfigurationError("CartesianTopology: size must be >0")
        elif self.expected_neighbors < 0:
            raise ConfigurationError("CartesianTopology: expected_neighbors can not be negative")
        elif self.expected_neighbors > self.size:
            raise ConfigurationError("CartesianTopology: expected_neighbors can not exceed size")

        self.graph = self.build_graph(size=self.size,
                                      expected_neighbors=self.expected_neighbors,
                                      periodic=self.periodic)

        if self.remove_disconnected and len(self.graph.nodes()) < self.size:
            self.relabel_nodes()

    def build_graph(self, size=0, expected_neighbors=0,
                    periodic=False):
        """Build the graph

        Parameters:

        *size*
            The number of nodes to be in the graph
        *expected_neighbors*
            The expected degree of each node in the graph
        *periodic*
            Whether or not to use periodic boundary conditions

        """

        # Calculate the distance required to yield the expected # neighbors
        if size == 1:
            radius = 1
        else:
            radius = sqrt( (expected_neighbors / (size - 1.0)) / pi)

        # Create bins in which to put node so we only check a fraction of
        # candidate neighbors
        num_bins = int(ceil(1/radius))
        neighbor_bins = []
        for i in range(num_bins):
            neighbor_bins.append([])
            for j in range(num_bins):
                neighbor_bins[i].append([])

        G = nx.empty_graph()
        G.name = "Cartesian Topology Graph"
        G.add_nodes_from(list(range(size)))

        # Create the collection of nodes and put them into bins with
        # candidate neighbors
        _rndm = random.random
        for n in G.nodes():
            xcoord = _rndm()
            ycoord = _rndm()
            G.node[n]['coords'] = (xcoord, ycoord)

            # Put node into bin with candidate neighbors
            bin_x = int(floor(xcoord/radius))
            bin_y = int(floor(ycoord/radius))
            neighbor_bins[bin_x][bin_y].append(n)

        # Find actual neighbors and create edges between nodes
        for x in range(num_bins):
            for y in range(num_bins):

                # Get all potential neighbors (those in adjacent bins)
                potentials = []
                for px in range(x-1, x+1+1):
                    if (periodic == False and
                        (px < 0 or px >= num_bins)):
                        continue

                    for py in range(y-y, y+1+1):
                        if (periodic == False and
                            (py < 0 or py >= num_bins)):
                            continue

                        potentials += neighbor_bins[px % num_bins][py % num_bins]

                for node in neighbor_bins[x][y]:
                    node_coords = G.node[node]['coords']
                    for potential in potentials:
                        p_coords = G.node[potential]['coords']
                        if (self.within_range(node_coords, p_coords, radius,
                                              periodic) and
                            node != potential):
                            G.add_edge(node, potential)

                    if G.degree(node) == 0:
                        if self.remove_disconnected:
                            G.remove_node(node)
                            neighbor_bins[x][y].remove(node)
                        else:
                            G.add_edge(node, random.choice(potentials))

                neighbor_bins[x][y] = []

        return G

    def within_range(self, node1, node2, distance, periodic):
        """Determine whether or not two nodes are within a given distance from
        each other

        Parameters:

        *node1*
            The first node (tuple)
        *node2*
            The second node (tuple)
        *distance*
            The threshold distance 
        *periodic*
            Whether or not periodic boundary conditions are used.

        """

        return euclidean_distance(node1, node2, periodic) < distance

    def add_node(self, id=-1, neighbors=[]):
        """Add a node to the graph.  Not supported by this topology type"""
        raise ConfigurationError("add_node is not supported by CartesianTopology")
        return

    def remove_node(self, id):
        """Remove a node from the graph.  Not supported by this topology
        type"""
        raise ConfigurationError("remove_node is not supported by CartesianTopology")
        return

    def add_edge(self, src, dest):
        """Add an edge to the graph.  Not supported by this topology type"""
        raise ConfigurationError("add_edge is not supported by CartesianTopology")
        return

    def remove_edge(self, src, dest):
        """Remove an edge from the graph.  Not supported by this topology
        type"""
        raise ConfigurationError("remove_edge is not supported by CartesianTopology")
        return
