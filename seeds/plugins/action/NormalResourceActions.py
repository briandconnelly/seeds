# -*- coding: utf-8 -*-
"""
Suite of Actions to change properties of a given NormalResource in all
populations
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.Action import *


class AdjustNormalResource(Action):

    """ Adjust a given NormalResource.  This could change the current level,
    the inflow amount, or the outflow rate.


    Configuration: All configuration options should be specified in a
    AdjustNormalResource block.

    epoch_start
        The epoch at which the Action starts executing
    epoch_end
        The epoch at which the Action stops executing
    frequency
        The frequency at which the Action is executed.  For example, if
        frequency=2, then the Action is executed at every other epoch.
    priority
        Priority of this Action.  Higher priority Actions run first. (default
        0)
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
        setdecay - Set the decay of resource to <value>
    value
        Value corresponding to the action

    Example:

    [AdjustNormalResource]
    epoch_start = 3
    epoch_end = 100
    frequency = 2
    resource = glucose
    type = add
    value = 1.2

    """
    def __init__(self, world):
        """Initialize the AdjustNormalResource object based on values in
        [AdjustNormalResource] config block
        
        """

        super(AdjustNormalResource, self).__init__(world)

        self.epoch_start = self.world.config.getint('AdjustNormalResource', 'epoch_start', 0)
        self.epoch_end = self.world.config.getint('AdjustNormalResource', 'epoch_end', default=self.world.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.world.config.getint('AdjustNormalResource', 'frequency', 1)
        self.priority = self.world.config.getint('AdjustNormalResource', 'priority', 0)

        self.resource = self.world.config.get('AdjustNormalResource', 'resource')
        self.type = self.world.config.get('AdjustNormalResource', 'type')
        self.value = self.world.config.getfloat('AdjustNormalResource', 'value', 0.0)

        if (self.type != 'add' and self.type != 'remove' and
            self.type != 'clear' and self.type != 'set' and
            self.type != 'setinflow' and self.type != 'setoutflow' and
            self.type != 'setdecay'):
            print 'Error: Invalid type for AdjustNormalResource'
      
    def update(self):
        """Adjust the appropriate resource accordingly"""
        if self.skip_update():
	        return

        for pop in self.world.populations:
            for cell in pop.cells:
                res = cell.resource_manager.get_resource(self.resource)
                # TODO: make sure resource is Normal

                if self.type == 'add':
                    if res != None:
                        res.set_level(res.level + self.value)
                elif self.type == 'remove':
                    if res != None:
                        res.set_level(res.level - self.value)
                elif self.type == 'clear':
                    if res != None:
                        res.level = 0
                        res.set_level(0)
                elif self.type == 'set':
                    if res != None:
                        res.set_level(self.value)
                elif self.type == 'setinflow':
                    if res != None:
                        res.set_inflow(self.value)
                elif self.type == 'setoutflow':
                    if res != None:
                        res.set_outflow(self.value)
                elif self.type == 'setdecay':
                    if res != None:
                        res.set_decay(self.value)

