# -*- coding: utf-8 -*-
"""
Topology in which the location of each Cell is represented by points randomly
placed on a 2D plane.  Each Cell is connected to a configured expected number
of neighbors.

This topology was originally presented and used used in the publication:

    B.D. Connelly, L. Zaman, C. Ofria, and P.K. McKinley, "Social structure and
    the maintenance of biodiversity," in Proceedings of the 12th International
    Conference on the Synthesis and Simulation of Living Systems (ALIFE), pp.
    461-468, 2010.

"""

__author__ = "Luis Zaman <zamanlui@msu.edu>"
__version__ = "1.0.2"
__credits__ = "Luis Zaman, Brian Connelly, Philip McKinley, Charles Ofria"

import random
import math

from seeds.CellManager import *
from seeds.topology.Topology import *


class CartesianTopology(Topology):
    """
    Topology based on points in Cartesian space on a 2D plane

    Points are placed randomly on a unit two-dimensional Cartesian plane.
    Each cell is connected to those cells that fall within a given distance.
    This distance is calculated to yield an expected number of neighbors
    equal to the expected_neighbors configuration parameter.

    Configuration: All configuration parameters are specified in a
        [CartesianTopology] block.

    size
        Total number of Cells in the topology (Integer)
    periodic_boundaries
        Whether or not to use periodic boundary conditions, which connects the
        edges of the plane, forming a torus. (Boolean)
    expected_neighbors
        The number of neighbors (expected) each cell will have.
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

    def __init__(self, world, id):
        """Initialize a CartesianTopology object

        Parameters:

        *world*
            A reference to the World
        *id*
            A unique ID assigned to the created CartesianTopology

        """

        Topology.__init__(self, world, id)
        self.size = self.world.config.getint('CartesianTopology', 'size')
        self.periodic_boundaries = self.world.config.getboolean('CartesianTopology', 'periodic_boundaries', default=False)
        self.expected_neighbors = self.world.config.getint('CartesianTopology', 'expected_neighbors')
        self.remove_disconnected = self.world.config.getboolean('CartesianTopology', 'remove_disconnected', default=True)

        self.graph = self.build_graph(size=self.size,
                                      expected_neighbors=self.expected_neighbors,
                                      periodic_boundaries=self.periodic_boundaries)

        # TODO: what is 120??
        #if self.expected_neighbors != -1 and self.expected_neighbors > 1 and self.expected_neighbors < 120:
        #    self.radius = math.sqrt( (self.expected_neighbors / float(self.size - 1 )) / math.pi)

        

    def build_graph(self, size=0, expected_neighbors=0,
                    periodic_boundaries=False):
        # TODO: documentation
        # TODO: parameter checking


        # Calculate the distance required to yield the expected # neighbors
        radius = math.sqrt( (expected_neighbors / (size - 1.0)) / math.pi)

        # Create bins in which to put cells so we only check a fraction of
        # candidate neighbors
        num_bins = int(math.ceil(1/radius))
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
            G.node[n]['resource_manager'] = ResourceManager(self.world, self)
            G.node[n]['cell'] = self.cell_manager.newcell(n,n)
        
            xcoord = random.random()
            ycoord = random.random()
            G.node[n]['cell'].coords = (xcoord, ycoord)

            # Put node into bin with candidate neighbors
            bin_x = int(math.floor(xcoord/radius))
            bin_y = int(math.floor(ycoord/radius))
            neighbor_bins[bin_x][bin_y].append(n)


        # Find actual neighbors and create edges between nodes
        for x in xrange(num_bins):
            for y in xrange(num_bins):

                # Get all potential neighbors (those in adjacent bins)
                potentials = []
                for px in range(x-1, x+1+1):
                    if (periodic_boundaries == False and
                        (px < 0 or px >= num_bins)):
                        continue

                    for py in range(y-y, y+1+1):
                        if (periodic_boundaries == False and
                            (py < 0 or py >= num_bins)):
                            continue

                        potentials += neighbor_bins[px % num_bins][py % num_bins]

                for node in neighbor_bins[x][y]:
                    node_coords = G.node[node]['cell'].coords
                    for potential in potentials:
                        p_coords = G.node[potential]['cell'].coords
                        if (self.within_range(node_coords, p_coords, radius,
                                              periodic_boundaries) and
                            node != potential):
                            G.add_edge(node, potential)
                    if G.degree(node) == 0:
                        if self.remove_disconnected:
                            G.remove_node(node)
                        else:
                            G.add_edge(node, random.choice(potentials))

                neighbor_bins[x][y] = []

        return G


    def distance(self, node1, node2, periodic_boundaries):
        """TODO"""
        if periodic_boundaries:
            dx = abs(node1[0] - node2[0])
            dist_x = min(dx, 1-dx)
            dy = abs(node1[1] - node2[1])
            dist_y = min(dy, 1-dy)
        else:
            dist_x = node1[0] - node2[0]
            dist_y = node1[1] - node2[1]

        return math.sqrt(dist_x**2 + dist_y**2)

    def within_range(self, node1, node2, radius, periodic_boundaries):
        """TODO"""
        return self.distance(node1, node2, periodic_boundaries) < radius

