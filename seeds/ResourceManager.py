# -*- coding: utf-8 -*-
"""
Handle a collection of Resource objects in a Cell
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import re

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
            match = re.match("Resource:(?P<resname>[a-zA-Z_0-9]+)", res)
            if match != None:
                name = match.group("resname")
                type = self.world.config.get(res, "type", default="NormalResource")
                available = self.world.config.getboolean(res, "available", default="True")

                if self.world.plugin_manager.plugin_exists(type):
                    oref = self.world.plugin_manager.get_plugin(type)
                    if oref == None:
                        print "Error: Couldn't find object ref for Resource type %s" % (self.type)
                    elif not issubclass(oref, Resource):
                        print "Error: Plugin %s is not an instance of Resource type" % (self.type)
                    else:
                        r = oref(world=self.world, name=name, available=available)
                        self.resources.append(r)
                else:
                    print 'Error: Unknown Resource type %s' % (type)


# Based on this, create a "ResourceGrid"--lattice (or plugin???) of Resources
#  - for each node in the graph, add a resource property

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
                return res.get_level

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

