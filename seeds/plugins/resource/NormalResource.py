# -*- coding: utf-8 -*-
"""
TODO
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.Resource import *


class NormalResource(Resource):
    """Environmental Resource class

    Properties:

    name
        Unique name of the resource
    available
        Whether or not the resource is currently available (default: True)
    level
        Current level of the resource
    inflow
        Amount of resource (in units) that flows into the environment per epoch
        for normal resources (default: 0.0)
    decay
        Amount of resource (in units) that flows out of the environment per epoch
        for normal resources (default: 0.0)
    outflow
        Fraction of resource (in percent) that flows into neighboring resource
        cells per epoch for normal resources (default: 0.0)
    initial
        The amount of resource (in units) present in the environment at the
        beginning for normal resources (default: 0.0)

    NormalResource Resources can be defined in config files using a
    [Resource:<uniquename>] section and using the NormalResource type.  For
    example:

        [Resource:glucose]
        type = NormalResource
        initial = 0
        inflow = 0.24
        outflow = 0.1
        decay = 0.1

    """
    def __init__(self, world, name=None, available=True):
        """ Initialize a NormalResource object

        Parameters:

        *world*
            A pointer to the World
        *name*
            A name for the resource
        *available*
            Whether or not the resource is available

        """
        super(NormalResource, self).__init__(world, name=name, available=available)

        self.inflow = self.world.config.getfloat(self.config_section, "inflow", default=0.0)
        self.outflow = self.world.config.getfloat(self.config_section, "outflow", default=0.0)
        self.decay = self.world.config.getfloat(self.config_section, "decay", default=0.0)
        self.initial = self.world.config.getfloat(self.config_section, "initial", default=0.0)

        self.level = self.initial * 1.0

        if self.inflow < 0:
            print "ERROR: invalid inflow"
        if self.outflow < 0 or self.outflow > 1:
            print "ERROR: invalid outflow"
        if self.decay < 0 or self.decay > 1:
            print "ERROR: invalid decay"
        

    def __str__(self):
        """Produce a string to be used when a NormalResource object is printed"""
        return "NormalResource [Name: %s][Level: %f][Inflow: %f][Outflow: %f][Decay: %f]" % (self.name, self.level, self.inflow, self.outflow, self.decay)

    def set_inflow(self, value):
        """Set the inflow amount of the resource

        Parameters:

        *value*
            The new inflow amount of the resoruce

        """
        self.inflow = value

    def set_outflow(self, value):
        """Set the outflow rate of the resource

        Parameters:

        *value*
            The new outflow rate of the resoruce

        """
        self.outflow = value

    def set_decay(self, value):
        """Set the decay rate of the resource

        Parameters:

        *value*
            The new decay rate of the resoruce

        """
        self.decay = value

    def set_initial(self, value):
        """Set the initial level of the resource

        Parameters:

        *value*
            The new initial level of the resoruce

        """
        self.initial = value

    def update(self):
        """Update the level of the resource.  Even if the resource is
        unavailable, the resource level will be updated.
        
        """
        # TODO: use outflow
        newlevel = (self.level * (1 - self.decay)) + self.inflow
        self.level = max(0, newlevel)

