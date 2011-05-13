# -*- coding: utf-8 -*-
"""
SineResource represents a resource whose levels fluctuate sinusoidally between
0 and two times the configured amplitude (i.e., the wave is shifted up one
amplitude).
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from math import sin, pi

from seeds.Resource import *

class SineResource(Resource):
    """Environmental Resource class

    Properties:

    name
        Unique name of the resource
    available
        Whether or not the resource is currently available (default: True)
    amplitude
        Defines the high value for the resource.  Minimum value will be 0, and
        maximum value will be 2*amplitude (default: 0.0).
    period
        Period the length of time (epochs) required to complete one cycle
        (integer values, units: epochs, default: 1).
    phase
        Phase specifies where in the cycle the resource level should be at
        epoch 0 (units: epochs, default: 0).

    SineResource Resources can be defined in config files using a
    [Resource:<uniquename>] section and type SineResource.  For example:

        [Resource:sun]
        type = SineResource
        amplitude = 3.2
        period = 100
        phase = 5

    """
    def __init__(self, world, name=None, available=True):
        """ Initialize a SineResource object

        Parameters:

        *world*
            A pointer to the World
        *name*
            A name for the resource
        *available*
            Whether or not the resource is available

        """
        super(SineResource, self).__init__(world, name=name, available=available)

        self.amplitude = self.world.config.getfloat(self.config_section, "amplitude", default=0.0)
        self.period = self.world.config.getint(self.config_section, "period", default=0)
        self.phase = self.world.config.getint(self.config_section, "phase", default=0)

        if self.amplitude < 0:
            print "ERROR: amplitude must be 0 or greater"
        if self.period <= 0:
            print "ERROR: period must greater than zero"
        if self.phase < 0:
            print "ERROR: phase must be 0 or greater"
        
    def __str__(self):
        """Produce a string to be used when a SineResource object is printed"""
        return "SineResource [Name: %s][Level: %f][Amplitude: %f][Period: %d][Phase: %d]" % (self.name, self.level, self.amplitude, self.period, self.phase)

    def set_amplitude(self, value):
        """Set the amplitude of the resource

        Parameters:

        *value*
            The new amplitude of the resoruce

        """
        self.amplitude = value

    def set_period(self, value):
        """Set the period of the resource

        Parameters:

        *value*
            The new period of the resoruce

        """
        self.period = value

    def set_phase(self, value):
        """Set the phase of the resource

        Parameters:

        *value*
            The new phase of the resoruce

        """
        self.phase = value

    def update(self):
        """Update the level of the resource.  Even if the resource is
        unavailable, the resource level will be updated.
        
        """

        position_radians = ((self.world.epoch * 1.0) / self.period) * 2 * pi
        phase_radians = ((self.phase * 1.0) / self.period) * 2 * pi
        self.level = (self.amplitude * sin(position_radians + phase_radians)) + self.amplitude

