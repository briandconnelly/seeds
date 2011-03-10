"""
Handle a collection of Resource objects in a Cell
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "0.9.0"
__credits__ = "Brian Connelly"


from lettuce.Resource import *

class ResourceManager(object):
    """
    Manage a Cell's Resources

    Each Cell object has a ResourceManager, which maintains a list of the
    Resources in that cell.

    """

    def __init__(self, world, topology):
        """Initialize a ResourceManager object

        Parameters:
        
        *world*
            A reference to the World
        *topology*
            The topology in which the Cell and Resources are located

        """
        self.world = world
        self.topology = topology
        self.resources = []

    def add_resource(self, newres):
        """Add a resource"""
        self.resources.append(newres)

    def get_level(self, name):
        """Get the level of a given resource

        Parameters:

        *name*
            The name of the Resource in question

        """
        for res in self.resources:
            if res.name == name:
                return res.level

    def get_resource(self, name):
        """Get the object associated with a given resource

        Parameters:

        *name*
            The name of the Resource in question

        """
        for res in self.resources:
            if res.name == name:
                return res

    def update(self):
        """Update all of the managed Resource objects"""
        for res in self.resources:
            res.update()

