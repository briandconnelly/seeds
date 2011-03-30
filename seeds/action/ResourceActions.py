# -*- coding: utf-8 -*-
"""
Suite of Actions to change properties of a given Resource in all
populations
"""
__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.2"
__credits__ = "Brian Connelly"


import csv

from seeds.Action import *

class AdjustResource(Action):

    """ Adjust a given Resource.  This could change the current level, the
    inflow amount, or the outflow rate.


    Configuration: All configuration options should be specified in a
    AdjustResource block.

    epoch_start
        The epoch at which the Action starts executing
    epoch_end
        The epoch at which the Action stops executing
    frequency
        The frequency at which the Action is executed.  For example, if
        frequency=2, then the Action is executed at every other epoch.
    resource
        The name of the resource to adjust
    type
        The action to take on that resource.  One of:

        add - Add <value> amount to current resource level
        remove - Remove <value> from current resource level
        clear - Remove all resource
        set - Set the current level of resource to <value>
        setinflow - Set the inflow of resource to <value>
        setoutflow - Set the outflow of resource to <value>
    value
        Value corresponding to the action

    Example:

    [AdjustResource]
    epoch_start = 3
    epoch_end = 100
    frequency = 2
    resource = glucose
    type = add
    value = 1.2

    """
    def __init__(self, world):
        """Initialize the AdjustResource object based on values in
        [AdjustResource] config block
        
        """

        Action.__init__(self, world)

        self.epoch_start = self.world.config.getint('AdjustResource', 'epoch_start', 0)
        self.epoch_end = self.world.config.getint('AdjustResource', 'epoch_end', default=self.world.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.world.config.getint('AdjustResource', 'frequency', 1)

        self.resource = self.world.config.get('AdjustResource', 'resource')
        self.type = self.world.config.get('AdjustResource', 'type')
        self.value = self.world.config.getfloat('AdjustResource', 'value', 0.0)

        if (self.type != 'add' and self.type != 'remove' and
            self.type != 'clear' and self.type != 'set' and
            self.type != 'setinflow' and self.type != 'setoutflow'):
            print 'Error: Invalid type for AdjustResource'
      
    def update(self):
        """Adjust the appropriate resource accordingly"""
        if self.skip_update():
	        return

        for top in self.world.topology_manager.topologies:
            for cell in top.cells:
                if self.type == 'add':
                    res = cell.resource_manager.get_resource(self.resource)
                    if res != None:
                        res.set_level(res.level + self.value)
                elif self.type == 'remove':
                    res = cell.resource_manager.get_resource(self.resource)
                    if res != None:
                        res.set_level(res.level - self.value)
                elif self.type == 'clear':
                    res = cell.resource_manager.get_resource(self.resource)
                    if res != None:
                        res.level = 0
                        res.set_level(0)
                elif self.type == 'set':
                    res = cell.resource_manager.get_resource(self.resource)
                    if res != None:
                        res.set_level(self.value)
                elif self.type == 'setinflow':
                    res = cell.resource_manager.get_resource(self.resource)
                    if res != None:
                        res.set_inflow(self.value)
                elif self.type == 'setoutflow':
                    res = cell.resource_manager.get_resource(self.resource)
                    if res != None:
                        res.set_outflow(self.value)

