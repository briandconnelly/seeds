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
            match = re.match("Resource:(?P<resname>[a-zA-Z_]+)", res)
            if match != None:
                name = match.group("resname")
                type = self.world.config.get(res, "type", default="normal")
                inflow = self.world.config.getfloat(res, "inflow", default=0.0)
                outflow = self.world.config.getfloat(res, "outflow", default=0.0)
                decay = self.world.config.getfloat(res, "decay", default=0.0)
                initial = self.world.config.getfloat(res, "initial", default=0.0)
                amplitude = self.world.config.getfloat(res, "amplitude", default=0.0)
                period = self.world.config.getfloat(res, "period", default=0.0)
                phase = self.world.config.getint(res, "phase", default=0)
                high = self.world.config.getfloat(res, "high", default=0.0)
                low = self.world.config.getfloat(res, "low", default=0.0)
                duty_cycle = self.world.config.getfloat(res, "duty_cycle", default=0.5)
                offset = self.world.config.getint(res, "offset", default=0)

                r = Resource(world=self.world, name=name, type=type,
                             initial=initial, inflow=inflow, outflow=outflow,
                             decay=decay, amplitude=amplitude, period=period,
                             phase=phase, high=high, low=low,
                             duty_cycle=duty_cycle, offset=offset)
                
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

