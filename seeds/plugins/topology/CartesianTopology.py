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

import random
from math import sqrt, floor, ceil, pi

from seeds.Topology import *


class CartesianTopology(Topology):
    """
    Topology based on points in Cartesian space on a 2D plane

    Points are placed randomly on a unit two-dimensional Cartesian plane.
    Each node is connected to those nodes that fall within a given distance.
    This distance is calculated to yield an expected number of neighbors
    equal to the expected_neighbors configuration parameter.

    Configuration: All configuration parameters are specified in a
      [CartesianTopology] block (unless otherwise specified with the
      config_section parameter).

    size
        Total number of nodes in the topology (Integer)
    periodic_boundaries
        Whether or not to use periodic boundary conditions, which connects the
        edges of the plane, forming a torus. (Boolean)
    expected_neighbors
        The number of neighbors (expected) each node will have.
    remove_disconnected
        Whether or not to remove nodes that do not have neighbors within the
        calculated radius.  If False, node is connected to a randomly-chosen
        neighbor (Boolean.  Default: True)

    Example:

    [CartesianTopology]
    size = 100000
    periodic_boundaries = True
    expected_neighbors = 20

    """

    def __init__(self, experiment, config_section='CartesianTopology'):
        """Initialize a CartesianTopology object

        Parameters:

        *experiment*
            A reference to the Experiment
        *config_section*
            The name of the section in the configuration file that stores the
            configuration for this Topology

        """

        super(CartesianTopology, self).__init__(experiment, config_section=config_section)
        self.size = self.experiment.config.getint(self.config_section, 'size')
        self.periodic_boundaries = self.experiment.config.getboolean(self.config_section, 'periodic_boundaries', default=False)
        self.expected_neighbors = self.experiment.config.getint(self.config_section, 'expected_neighbors')
        self.remove_disconnected = self.experiment.config.getboolean(self.config_section, 'remove_disconnected', default=True)
        self.graph = self.build_graph(size=self.size,
                                      expected_neighbors=self.expected_neighbors,
                                      periodic_boundaries=self.periodic_boundaries)

    def build_graph(self, size=0, expected_neighbors=0,
                    periodic_boundaries=False):
        """Build the graph

        Parameters:

        *size*
            The number of nodes to be in the graph
        *expected_neighbors*
            The expected degree of each node in the graph
        *periodic_boundaries*
            Whether or not to use periodic boundary conditions

        """

        # Calculate the distance required to yield the expected # neighbors
        radius = sqrt( (expected_neighbors / (size - 1.0)) / pi)

        # Create bins in which to put node so we only check a fraction of
        # candidate neighbors
        num_bins = int(ceil(1/radius))
        neighbor_bins = []
        for i in xrange(num_bins):
            neighbor_bins.append([])
            for j in xrange(num_bins):
                neighbor_bins[i].append([])

        G = nx.empty_graph()
        G.name = "Cartesian Topology Graph"
        G.add_nodes_from(range(size))


        # Create the collection of nodes and put them into bins with
        # candidate neighbors
        for n in G.nodes():
            xcoord = random.random()
            ycoord = random.random()
            G.node[n]['coords'] = (xcoord, ycoord)

            # Put node into bin with candidate neighbors
            bin_x = int(floor(xcoord/radius))
            bin_y = int(floor(ycoord/radius))
            neighbor_bins[bin_x][bin_y].append(n)


        # Find actual neighbors and create edges between nodes
        for x in xrange(num_bins):
            for y in xrange(num_bins):

                # Get all potential neighbors (those in adjacent bins)
                potentials = []
                for px in xrange(x-1, x+1+1):
                    if (periodic_boundaries == False and
                        (px < 0 or px >= num_bins)):
                        continue

                    for py in xrange(y-y, y+1+1):
                        if (periodic_boundaries == False and
                            (py < 0 or py >= num_bins)):
                            continue

                        potentials += neighbor_bins[px % num_bins][py % num_bins]

                for node in neighbor_bins[x][y]:
                    node_coords = G.node[node]['coords']
                    for potential in potentials:
                        p_coords = G.node[potential]['coords']
                        if (self.within_range(node_coords, p_coords, radius,
                                              periodic_boundaries) and
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


    def distance(self, node1, node2, periodic_boundaries):
        """Calculate the distance between two nodes

        Parameters:

        *node1*
            The first node (tuple)
        *node2*
            The second node (tuple)
        *periodic_boundaries*
            Whether or not periodic boundary conditions are used.

        """

        if periodic_boundaries:
            dx = abs(node1[0] - node2[0])
            dist_x = min(dx, 1-dx)
            dy = abs(node1[1] - node2[1])
            dist_y = min(dy, 1-dy)
        else:
            dist_x = node1[0] - node2[0]
            dist_y = node1[1] - node2[1]

        return sqrt(dist_x**2 + dist_y**2)


    def within_range(self, node1, node2, distance, periodic_boundaries):
        """Determine whether or not two nodes are within a given distance from
        each other

        Parameters:

        *node1*
            The first node (tuple)
        *node2*
            The second node (tuple)
        *distance*
            The threshold distance 
        *periodic_boundaries*
            Whether or not periodic boundary conditions are used.

        """

        return self.distance(node1, node2, periodic_boundaries) < distance

