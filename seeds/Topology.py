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

from math import sqrt

import networkx as nx
from networkx.exception import *

from seeds.SEEDSError import *
from seeds.utils.geometry import euclidean_distance


class Topology(object):
    """
    All topologies contain properties:

        config_section
            The name of the section in the configuration file that stores the
            configuration for this Topology.  This will likely need to be set
            by each Topology plugin (e.g., CartesianTopology:label1).
        graph
            A NetworkX graph object defining the connections between cells.
        experiment
            Reference to the Experiment in which it exists
        periodic
            Whether or not to use periodic boundary conditions, which connects
            the edges of the space (default: False)
        label
            A unique label identifying a configuration for the Topology

    """

    def __init__(self, experiment, label=None):
        """Initialize a Topology object.

        The topology will have no cells and an empty graph

        Parameters:

        *experiment*
            A reference to the Experiment
        *label*
            A unique label identifying a configuration for the Topology

        """

        self.experiment = experiment
        self.graph = nx.Graph()
        self.periodic = False
        self.label = label
        self.config_section = None
        self.dimensions = 0

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

    def node_distance(self, src, dest):
        """Calculate the Euclidean distance between the given two nodes using
        their 'coords' properties

        Parameters:

        *src*
            The first node ID
        *dest*
            The second node ID

        If either node does not exist, NonExistentNodeError will be raised

        """

        if src not in self.graph.nodes():
            raise NonExistentNodeError(src)
        elif dest not in self.graph.nodes():
            raise NonExistentNodeError(dest)

        return euclidean_distance(self.graph.node[src]['coords'],
                                  self.graph.node[dest]['coords'],
                                  periodic=self.periodic)

    def add_node(self, id=None, neighbors=[], coords=None):
        """Add a node to the graph.  Topologies that do not wish to support
        this should redefine this method to do nothing.  This method will
        not place a Cell or ResourceCell in the newly-created node.  That
        will need to be done separately.

        The general convention in SEEDS is for all nodes to have coordinates in
        unit Cartesian space.  These coordinates are stored as a tuple as a
        node property named 'coords'.  New nodes should be given coordinates
        appropriately.

        Example:

            self.graph.node[id]['coords'] = (0.21, 0.00313)

        Parameters:

        id
            The ID to use for the new node.  If none is specified, the
            ID used will be the current largest ID in the graph plus 1.
        neighbors
            An optional list of node IDs that will be connected to the new node
            via an edge. NonExistentNodeError will be raised if any of these
            nodes do not exist.
        coords
            A tuple containing the coordinates of the new node.  The dimensions
            of this tuple should match the number of dimensions represented in
            the topology.  If no coordinates are provided, the origin will be
            used (0,0).

        """

        if not id:
            id = max(self.graph.nodes()) + 1
        if not coords:
            coords = tuple([0] * self.dimensions)
        elif self.dimensions != len(coords):
            raise SEEDSError("Cell coordinates do not match topology dimensions")

        self.graph.add_node(id)
        self.graph.node[id]['coords'] = coords

        for n in neighbors:
            if n not in self.graph.nodes():
                raise NonExistentNodeError(n)
            self.graph.add_edge(id, n)

        self.size = len(self.graph)

    def remove_node(self, id):
        """Remove a node from the graph.  Topologies that do not wish to
        support this should redefine this method to do nothing.  This method
        will not perform teardown actions for any Cell or ResourceCell objects
        residing in the node.  That will need to be done separately (before
        remove_node is called).  Any edges associated with the node will also
        be removed.

        Parameters:

        id
            The ID to use of the node to be deleted.

        """

        try:
            self.graph.remove_node(id)
            self.size = len(self.graph)
        except NetworkXError as err:
            raise NonExistentNodeError(id)

    def add_edge(self, src, dest):
        """Add an edge between the given two nodes.  Although NetworkX creates
        new node(s) when non-existent nodes are given as arguments to
        add_edge(), this method will raise an exception (NonExistentNodeError)
        if either of the given nodes does not exist.

        Parameters:

        src
            ID of the source node
        dest
            ID of the dest node

        """

        if src not in self.graph.nodes():
            raise NonExistentNodeError(src)
        elif dest not in self.graph.nodes():
            raise NonExistentNodeError(dest)
        else:
            self.graph.add_edge(src, dest)

    def remove_edge(self, src, dest):
        """Remove the edge between the given two nodes.  This method will raise
        an exception (NonExistentEdgeError) if either of the given nodes does
        not exist.

        Parameters:

        src
            ID of the source node
        dest
            ID of the dest node

        """

        try:
            self.graph.remove_edge(src, dest)
        except NetworkXError as err:
            raise NonExistentEdgeError(src, dest)

    def get_nearest_node(self, coords, n=1):
        """Return a list of  the node(s) located nearest the given coordinates

        Parameters:

        coords
            Tuple defining the point in question.  The number of dimensions
            should match the number of dimensions of the topology.
        n
            The number of nearest neighbors to find

        """

        if not coords or len(coords) < 1:
            return
        elif n < 1:
            # TODO: print warning or throw an exception 
            # TODO: search the KD tree for the coordinates
            return

    def relabel_nodes(self):
        """Relabel the nodes in the graph so that labels are numbers from
        0..len(graph) with no gaps.  This is done, for instance, after
        disconnected nodes have been removed from the graph.
        """
        M = {}
        for i in range(len(self.graph.nodes())):
            M[self.graph.nodes()[i]] = i
        
        self.graph = nx.relabel_nodes(self.graph, M)
