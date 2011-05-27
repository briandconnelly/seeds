# -*- coding: utf-8 -*-
"""
SquareResource represents a resource whose levels fluctuate between two
specific values.  These values and the fraction of time spent in either state
can be configured.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.Resource import *


class SquareResource(Resource):
    """Environmental Resource class

    Properties:

    name
        Unique name of the resource
    available
        Whether or not the resource is currently available (default: True)
    period
        Period is the length of time (epochs) required to complete one cycle
        (integer values, units: epochs, default: 0).
    high
        High specifies the maximum value of the resource, which occurs in the
        high state (default: 0.0).
    low
        Low specifies the minimum value of the resource, which occurs in the
        low state (default: 0.0).
    duty_cycle
        Duty cycle is the fraction of one period that a resource spends in high
        state (default: 0.5).
    offset
        Offset defines the amount of time in epochs before the first high state
        is encountered (default: 0).

    SquareResource Resources can be defined in config files using a
    [Resource:<uniquename>] section and SquareResource type.  For example:

        [Resource:enzyme]
        type = SquareResource
        period = 100
        high = 5.8
        low = 0.0
        duty_cycle = 0.33
        offset = 5

    """
    def __init__(self, experiment, name=None, available=True):
        """ Initialize a SquareResource object

        Parameters:

        *experiment*
            A pointer to the Experiment
        *name*
            A name for the Resource
        *available*
            Whether or not the resource is available

        """
        super(SquareResource, self).__init__(experiment, name=name, available=available)

        self.period = self.experiment.config.getint(self.config_section, "period", default=0)
        self.high = self.experiment.config.getfloat(self.config_section, "high", default=0.0)
        self.low = self.experiment.config.getfloat(self.config_section, "low", default=0.0)
        self.duty_cycle = self.experiment.config.getfloat(self.config_section, "duty_cycle", default=0.5)
        self.offset = self.experiment.config.getint(self.config_section, "offset", default=0)

        if self.period <= 0:
            print "ERROR: period must greater than 0"
        if self.high < self.low:
            print "ERROR: high value must be greater than or equal to low value"
        
    def __str__(self):
        """Produce a string to be used when a SquareResource object is printed"""
        return "SquareResource [Name: %s][Level: %f][Offset: %f][Period: %d][High: %f][Low: %f][Duty Cycle: %f]" % (self.name, self.level, self.offset, self.high, self.low, self.duty_cycle)

       
    def set_offset(self, value):
        """Set the offset of the resource

        Parameters:

        *value*
            The new offset of the resoruce

        """

        self.offset = value

    def set_period(self, value):
        """Set the period of the resource

        Parameters:

        *value*
            The new period of the resoruce

        """

        self.period = value

    def set_high(self, value):
        """Set the high of the resource

        Parameters:

        *value*
            The new high of the resoruce

        """

        self.high = value

    def set_low(self, value):
        """Set the low of the resource

        Parameters:

        *value*
            The new low of the resoruce

        """

        self.low = value

    def set_duty_cycle(self, value):
        """Set the duty_cycle of the resource

        Parameters:

        *value*
            The new duty_cycle of the resoruce

        """

        self.duty_cycle = value


    def update(self):
        """Update the level of the resource.  Even if the resource is
        unavailable, the resource level will be updated.
        
        """

        position = ((self.experiment.epoch - self.offset) % (self.period)) / (self.period * 1.0)

        if position < self.duty_cycle:
            self.level = self.high
        else:
            self.level = self.low

