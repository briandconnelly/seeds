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

import networkx as nx
from networkx.exception import *

from seeds.SEEDSError import *


class Topology(object):
    """
    All topologies contain properties:

        config_section
            The name of the section in the configuration file that stores the
            configuration for this Topology
        graph
            A NetworkX graph object defining the connections between cells.
        experiment
            Reference to the Experiment in which it exists

    """

    def __init__(self, experiment, config_section=None):
        """Initialize a Topology object.

        The topology will have no cells and an empty graph

        Parameters:

        *experiment*
            A reference to the Experiment
        *config_section*
            The name of the section in the configuration file that stores the
            configuration for this Topology

        """

        self.experiment = experiment
        self.graph = nx.Graph()
        self.config_section = config_section

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

    def add_node(self, id=-1, neighbors=[]):
        """Add a node to the graph.  Topologies that do not wish to support
        this should redefine this method to do nothing.  This method will
        not place a Cell or ResourceType in the newly-created node.  That
        will need to be done separately.

        The general convention in SEEDS is for all nodes to have coordinates in
        unit Cartesian space.  These coordinates are stored as a tuple as a
        node property named 'coords'.  New nodes should be given coordinates
        appropriately.

        Example:

            self.graph.node[id]['coords'] = (0.21, 0.00313)

        Parameters:

        id
            The ID to use for the new node.  If none is specified (or -1), the
            ID used will be the current largest ID in the graph plus 1.
        neighbors
            An optional list of node IDs that will be connected to the new node
            via an edge. NonExistentNodeError will be raised if any of these
            nodes do not exist.

        """

        if id == -1:
            self.graph.add_node(max(self.graph.nodes()) + 1)
        else:
            self.graph.add_node(id)

        for n in neighbors:
            if n not in self.graph.nodes():
                raise NonExistentNodeError(n)
            self.graph.add_edge(id, n)

    def remove_node(self, id):
        """Remove a node from the graph.  Topologies that do not wish to
        support this should redefine this method to do nothing.  This method
        will not perform teardown actions for any Cell or ResourceType objects
        residing in the node.  That will need to be done separately (before
        remove_node is called).  Any edges associated with the node will also
        be removed.

        Parameters:

        id
            The ID to use of the node to be deleted.

        """

        try:
            self.graph.remove_node(id)
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

