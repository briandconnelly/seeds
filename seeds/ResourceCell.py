# -*- coding: utf-8 -*-

""" In SEEDS, environmental Resources are comprised of a graph of nodes, each
of which contains one ResourceCell object.  ResourceCells define the way in
which the defined resource behaves at that point in space.

TODO: more understandable description

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


class ResourceCell(object):
    """Interface for ResourceCell objects.  A ResourceCell object represents a
    Resource at a particular location in space.

    Properties:
    
    *config_section*
        The name of the section in the configuration file where parameter
        values are set
    *experiment*
        A reference to the experiment being run
    *id*
        A unique ID for this ResourceCell object
    *level*
        The level of the Resource at this point
    *resource*
        A reference to the Resource to which this ResourceCell belongs
    *neighbors*
        A list of neighbor ResourceCells.  A neighbor is a ResourceCell that
        exists on an adjacent node.

    """

    def __init__(self, experiment, resource, config_section, id):
        """Initialize the ResourceCell object"""
        self.experiment = experiment
        self.resource = resource
        self.level = 0.0
        self.config_section = config_section
        self.id = id
        self.neighbors = []

    def __str__(self):
        """Return a string for when a ResourceCell object is printed"""
        return 'ResourceCell Object (Level: %f)' % (self.level)

    # By default, comparisons between two ResourceCell objects will be done
    # solely using their levels
    __lt__ = lambda self, other: self.level < other.level
    __le__ = lambda self, other: self.level <= other.level
    __eq__ = lambda self, other: self.level == other.level
    __ne__ = lambda self, other: self.level != other.level
    __gt__ = lambda self, other: self.level > other.level
    __ge__ = lambda self, other: self.level >= other.level

    def update(self):
        """Update the ResourceCell object in the node"""
        pass

    def teardown(self):
        """Perform any necessary cleanup at the end of the experiment"""
        pass

    def get_neighbors(self):
        """Get a list of neighboring ResourceCells"""
        return [self.resource.topology.graph.node[n]['resource'] for n in self.resource.topology.get_neighbors(self.id)]

    def update_neighbors(self):
        """Update the list of neighboring ResourceCells"""
        self.neighbors = self.get_neighbors()

    def coords(self):
        """Get the coordinates of the ResourceCell in space"""
        return self.resource.topology.graph.node[self.id]['coords']

    def get_neighbor_distance(self, neighbor):
        """Get the Cartesian distance to the given neighbor ResourceCell"""
        return self.resource.resourcetype_distance(self, neighbor)

    def get_neighbor_distances(self):
        """Get an array of distances to all neighbors"""
        return [self.get_neighbor_distance(n) for n in self.get_neighbors()]
