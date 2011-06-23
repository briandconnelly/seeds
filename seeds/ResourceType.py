# -*- coding: utf-8 -*-

""" In SEEDS, environmental Resources are comprised of a graph of nodes, each
of which contains one ResourceType object.  ResourceTypes define the way in
which the defined resource behaves at that point in space.

TODO: more understandable description

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


class ResourceType(object):
    """Interface for ResourceType objects.  A ResourceType object represents a
    Resource at a particular location in space.

    Properties:
    
    *experiment*
        A reference to the experiment being run
    *resource*
        A reference to the Resource to which this ResourceType belongs
    *config_section*
        The name of the section in the configuration file where parameter
        values are set
    *id*
        A unique ID for this ResourceType object

    """

    def __init__(self, experiment, resource, config_section, id):
        """Initialize the ResourceType object"""
        self.experiment = experiment
        self.resource = resource
        self.level = 0.0
        self.config_section = config_section
        self.id = id

    def __str__(self):
        """Return a string for when a ResourceType object is printed"""
        return 'ResourceType Object (Level: %f)' % (self.level)

    def update(self):
        """Update the ResourceType object in the node"""
        pass

    def teardown(self):
        """Perform any necessary cleanup at the end of the experiment"""
        pass

    def get_neighbors(self):
        """Get a list of neighboring ResourceTypes"""
        return [self.resource.topology.graph.node[n]['resource'] for n in self.resource.topology.get_neighbors(self.id)]

    def coords(self):
        """Get the coordinates of the ResourceType in space"""
        return self.resource.topology.graph.node[self.id]['coords']

    def get_neighbor_distance(self, neighbor):
        """Get the Cartesian distance to the given neighbor ResourceType"""
        return self.resource.resourcetype_distance(self, neighbor)

    def get_neighbor_distances(self):
        """Get an array of distances to all neighbors"""
        return [self.get_neighbor_distance(n) for n in self.get_neighbors()]

