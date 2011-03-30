# -*- coding: utf-8 -*-
"""
Provide resources which the cells can consume or produce.

For each configured resource, a Resource object is placed into each node in the
topology. These Resource objects are updated whenever that node is updated.

Additionally, Resources can be manipulated with Actions.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.1"
__credits__ = "Brian Connelly"

class Resource(object):
    """Environmental Resource class

    Properties:

    name
        Unique name of the resource
    level
        current level of the resource
    inflow
        amount of resource (in units) that flows into the
        environment per epoch (default: 0.0)
    outflow
        fraction of resource (in percent) that flows out of
        the environment per epoch (default: 0.0)
    initial
        the amount of resource (in units) present in the
        environment at the beginning (default: 0.0)

    Resources can be defined in config files using a [Resource:<uniquename>]
    section.  For example:

        [Resource:glucose]
        initial = 0
        inflow = 0.24
        outflow = 0.1

    At each update, the outflow amount is removed first, then inflow is added.
    This leads to equilibrium levels (if unpreturbed) of inflow/outflow

    """

    def __init__(self, name=None, inflow=0.0, outflow=0.0, initial=0.0):
        """ Initialize a Resource object

        Parameters:

        *name*
            A name for the resource
        *inflow*
            An inflow amount (in units) that flows into the cell at each update
        *outflow*
            An amount (percentage of current level) of resource that flows out
            of the cell at each update
        *initial*
            The amount of resource present in the cell at the beginning of the
            experiment

        """

        if name != None:
            self.name = name
        else:
            print "Error: Must supply Resource name"

        self.initial = initial
        self.level = self.initial * 1.0
        self.inflow = inflow
        self.outflow = outflow

        if self.outflow < 0 or self.outflow > 1:
            print "ERROR: invalid outflow"

    def __str__(self):
        """Produce a string to be used when a Resource object is printed"""
        return "Resource [Name: %s][Level: %f][Inflow: %f][Outflow: %f]" % (self.name, self.level, self.inflow, self.outflow)

    def set_name(self, value):
        """Set the name of the resource

        Parameters:

        *value*
            The new name for the resoruce

        """
        self.name = value

    def set_level(self, value):
        """Set the level of the resource

        Parameters:

        *value*
            The new level of the resoruce

        """
        self.level = value

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

    def set_initial(self, value):
        """Set the initial level of the resource

        Parameters:

        *value*
            The new initial level of the resoruce

        """
        self.initial = value

    def update(self):
        """Update the level of the resource"""
        newlevel = (self.level * (1 - self.outflow)) + self.inflow
        self.level = max(0, newlevel)

