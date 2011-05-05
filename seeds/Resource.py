# -*- coding: utf-8 -*-
"""
Provide resources which the cells can consume or produce.

For each configured resource, a Resource object is placed into each node in the
topology. These Resource objects are updated whenever that node is updated.

Additionally, Resources can be manipulated with Actions.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from math import sin, pi, floor

class Resource(object):
    """Environmental Resource class

    Properties:

    name
        Unique name of the resource
    type
        The type of resource to use.  One of:
        - normal (default): resource with inflow, outflow, and decay.
          Additionally, an initial level can be specified.
        - sine: Resource level is a sinusoidal function with amplitude,
          period, and phase.  Note that the value is shifted up by
          one amplitude to yield values in the range [0, 2*A].
        - square: Resource level is a square wave that fluctuates between a
          high and low value during a defined period.  An additional duty_cycle
          can be specified which states the percentage of time per period spent
          in high state.
    available
        Whether or not the resource is currently available (default: True)
    level
        Current level of the resource
    inflow
        Amount of resource (in units) that flows into the environment per epoch
        for normal resources (default: 0.0)
    outflow
        Amount of resource (in units) that flows out of the environment per epoch
        for normal resources (default: 0.0)
    decay
        Fraction of resource (in percent) that flows into neighboring resource
        cells per epoch for normal resources (default: 0.0)
    initial
        The amount of resource (in units) present in the environment at the
        beginning for normal resources (default: 0.0)
    amplitude
        Amplitude for Sine resources.  Minimum value will be 0, and maximum
        value will be 2*amplitude (default: 0.0).
    period
        Period for Sine and Square resources.  This is the length of time
        (epochs) required to complete one cycle (integer values, units: epochs,
        default: 0).
    phase
        Phase for Sine resources.  This specifies where in the cycle the
        resource level should be at epoch 0 (units: epochs, default: 0.0).
    high
        High value for Square resources.  This specifies the maximum value of
        the resource, which occurs in the high state (default: 0.0).
    low
        Low value for Square resources.  This specifies the minimum value of
        the resource, which occurs in the low state (default: 0.0).
    duty_cycle
        Duty cycle is the fraction of one period tha a Square resource spends
        in high state (default: 0.5).
    offset
        Offset for Square resources.  Offset defines the amount of time in
        epochs before the first high state is encountered.

    Resources can be defined in config files using a [Resource:<uniquename>]
    section.  For example:

        [Resource:glucose]
        type = normal
        initial = 0
        inflow = 0.24
        outflow = 0.1
        decay = 0.1

        [Resource:onoff]
        type = square
        high = 1
        low = 0
        period = 10
        duty_cycle = 0.5
        offset = 2

    TODO: update this documentation
    At each update, the outflow amount is removed first, then inflow is added.
    This leads to equilibrium levels (if unpreturbed) of inflow/outflow

    """

    def __init__(self, world, name=None, type="normal", available=True,
        inflow=0.0, outflow=0.0, decay=0.0, initial=0.0, amplitude=0.0,
        period=0.0, phase=0.0, high=0.0, low=0.0, duty_cycle=0.5, offset=0):
        """ Initialize a Resource object

        Parameters:

        *world*
            A pointer to the World
        *name*
            A name for the resource
        *type*
            The type of resource to use.  One of:
            - normal (default): resource with inflow, outflow, and decay.
              Additionally, an initial level can be specified.
            - sine: Resource level is a sinusoidal function with amplitude,
              period, and phase.  Note that values are shifted up by one
              amplitude to yield values in the range [0, 2*A].
            - square: Resource level is a square wave that fluctuates between a
              high and low value during a defined period.  An additional
              duty_cycle can be specified which states the percentage of time
              per period spent in high state.
        *available*
            Whether or not the resource is currently available (default: True).
            When a resource is unavailable, get_level will return a level of
            0.0.
        *inflow*
            An inflow amount (in units) that flows into the cell at each update
        *outflow*
            An amount (percentage of current level) of resource that flows into
            neighboring resource cells of the cell at each update
        *decay*
            An amount (percentage of current level) of resource that flows out
            of the cell at each update
        *initial*
            The amount of resource present in the cell at the beginning of the
            experiment (default: 0.0)
        *amplitude*
            Amplitude for Sine resources.  Minimum value will be 0, and maximum
            value will be 2*amplitude (default: 0.0).
        *period*
            Period for Sine and Square resources.  This is the length of time
            (epochs) required to complete one cycle (integer values, units:
            epochs, default: 0).
        *phase*
            Phase for Sine resources.  This specifies where in the cycle the
            resource level should be at epoch 0 (units: epochs, default: 0.0).
        *high*
             High value for Square resources.  This specifies the maximum value
             of the resource, which occurs in the high state (default: 0.0).
        *low*
            Low value for Square resources.  This specifies the minimum value
            of the resource, which occurs in the low state (default: 0.0).
        *duty_cycle*
            Duty cycle is the fraction of one period tha a Square resource
            spends in high state (default: 0.5).
        *offset*
            Offset for Square resources.  Offset defines the amount of time
            (in epochs) before the first high state is encountered (default: 0).

        """

        self.world = world

        if name != None:
            self.name = name
        else:
            print "Error: Must supply Resource name"

        self.type = type
        self.available = available
        self.initial = initial
        self.level = self.initial * 1.0
        self.inflow = inflow
        self.outflow = outflow
        self.decay = decay
        self.amplitude = amplitude
        self.period = period
        self.phase = phase
        self.high = high
        self.low = low
        self.duty_cycle = duty_cycle
        self.offset = offset

        if self.type not in ["normal", "sine", "square"]:
            print "ERROR: invalid resource type '%s'.  Must be one of normal, sine, or square" % (self.type)

        if self.outflow < 0 or self.outflow > 1:
            print "ERROR: invalid outflow"
        
        if self.amplitude < 0:
            print "ERROR: amplitude must be 0 or greater"

        if self.period < 0:
            print "ERROR: period must be 0 or greater"

        if self.phase < 0:
            print "ERROR: phase must be 0 or greater"

        if self.low > self.high:
            print "ERROR: low state value should be greater than or equal to high state value"

        if self.duty_cycle < 0 or self.duty_cycle > 1:
            print "ERROR: duty cycle value must be between 0 and 1, inclusive"

    def __str__(self):
        """Produce a string to be used when a Resource object is printed"""
        return "Resource [Name: %s][Type: %s][Level: %f]" % (self.name, self.type, self.level)

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


    def get_level(self):
        """Return the current level of the resource.  If it is no available,
        0.0 will be returned.

        """

        if self.available:
            return self.level
        else:
            return 0.0

    def update(self):
        """Update the level of the resource.  Even if the resource is
        unavailable, the resource level will be updated.
        
        """
        if self.type == "normal":
            newlevel = (self.level * (1 - self.outflow)) + self.inflow
            self.level = max(0, newlevel)
        elif self.type == "sine":
            position_radians = ((self.world.epoch * 1.0) / self.period) * 2 * pi
            phase_radians = ((self.phase * 1.0) / self.period) * 2 * pi
            self.level = (self.amplitude * sin(position_radians + phase_radians)) + self.amplitude
        elif self.type == "square":
            position = ((self.world.epoch - self.offset) % (self.period)) / (self.period * 1.0)

            if position < self.duty_cycle:
                self.level = self.high
            else:
                self.level = self.low

