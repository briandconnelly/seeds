# -*- coding: utf-8 -*-
"""
Handle a collection of Resource objects in a Cell
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.1"
__credits__ = "Brian Connelly"


from seeds.Resource import *

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
        self.init_resources()

    def init_resources(self):
        """Initialize all resources that will be associated with this Cell"""
        for res in self.world.config.get_resource_sections():
            match = re.match("Resource:(?P<resname>[a-zA-Z_]+)", res)
            if match != None:
                name = match.group("resname")

                initial = self.world.config.getfloat(res, 'initial')
                inflow = self.world.config.getfloat(res, 'inflow')
                outflow = self.world.config.getfloat(res, 'outflow')

                r = Resource(name=name, initial=initial, inflow=inflow, outflow=outflow)
                self.add_resource(r)

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

