# -*- coding: utf-8 -*-
"""
SineResource represents a resource whose levels fluctuate sinusoidally between
0 and two times the configured amplitude (i.e., the wave is shifted up one
amplitude).
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from math import sin, pi

from seeds.Action import *
from seeds.ResourceCell import *
from seeds.SEEDSError import *
from seeds.utils.parsing import parse_int_rangelist


class SineResource(ResourceCell):
    """Environmental Resource class

    Properties:

    experiment
        A reference to the experiment being run
    resource
        A reference to the Resource to which this ResourceCell belongs
    config_section
        The name of the section in the configuration file where parameter
        values are set
    id
        A unique ID for this ResourceCell object
    name
        Unique name of the resource
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
    def __init__(self, experiment, resource, config_section, id):
        """ Initialize a SineResource object

        Parameters:

        *experiment*
            A pointer to the Experiment
        *resource*
            A pointer to the Resource of which this is a part
        *config_section*
            The name under which the configuration parameters are specified for
            this Resource
        *id*
            A unique ID for this node in the resource graph

        """
        super(SineResource, self).__init__(experiment=experiment,
                                           resource=resource,
                                           config_section=config_section,
                                           id=id)

        self.amplitude = self.experiment.config.getfloat(self.config_section, "amplitude", default=0.0)
        self.period = self.experiment.config.getint(self.config_section, "period", default=0)
        self.phase = self.experiment.config.getint(self.config_section, "phase", default=0)

        if self.amplitude < 0:
            raise ConfigurationError("SineResource: amplitude for '%s' must be at least 0" % (self.resource.name))
        elif self.period <= 0:
            raise ConfigurationError("SineResource: period for '%s' must be greater than 0" % (self.resource.name))
        elif self.phase < 0:
            # BDC: really, a negative phase should be ok...
            raise ConfigurationError("SineResource: phase for '%s' must be greater than 0" % (self.resource.name))

        # Set the initial level
        self.update()
        
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

        position_radians = ((self.experiment.epoch * 1.0) / self.period) * 2 * pi
        phase_radians = ((self.phase * 1.0) / self.period) * 2 * pi
        self.level = (self.amplitude * sin(position_radians + phase_radians)) + self.amplitude
        self.experiment.data['resources'][self.resource.name]['levels'][self.id] = self.level


class SetSineResourceProperties(Action):
    """ Action to set the properties (period, high, low, or duty cycle) of a
    SineResource resource

    Configuration is done in the [SetSineResourceProperties] section

    Configuration Options:

    epoch_start
        The epoch at which to start executing (default: 0)
    epoch_end
        The epoch at which to stop executing (default: end of experiment)
    frequency
        The frequency (epochs) at which to execute (default: 1)
    priority
        The priority of this action.  Actions with higher priority get run
        first.  (default: 0)
    resource
        The name of the resource whose availability to set
    cells
        A list of the ResourceCell cells whose inflow to set.  If none are
        specified, the inflows all cells will be set.
    period
        Period is the length of time (epochs) required to complete one cycle.
        If no value is specified, the period will not be altered.  (integer
        values, units: epochs)
    amplitude
        Amplitude specifies the amplitude of the resource.  If no value is
        specified, the high value will not be altered.

    Configuration Example:

    [SetSineResourceProperties]
    resource = glucose
    period = 100
    epoch_start = 0
    epoch_end = 100
    frequency = 1
    priority = 0

    """

    def __init__(self, experiment, label=None):
        """Initialize the SetSineResourceProperties Action"""

        super(SetSineResourceProperties, self).__init__(experiment,
                                                name="SetSineResourceProperties",
                                                label=label)

        self.threshold = self.experiment.config.getint(self.config_section, 'threshold', 0)
        self.epoch_start = self.experiment.config.getint(self.config_section, 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint(self.config_section, 'epoch_end',
                                                  default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint(self.config_section, 'frequency', 1)
        self.priority = self.experiment.config.getint(self.config_section, 'priority', 0)

        self.resource = self.experiment.config.get(self.config_section, 'resource')

        try:
            self.res = self.experiment.resources[self.resource]
        except KeyError:
            raise ConfigurationError("SetSinSinerceProperties: Resource '%s' is undefined" % (self.resource))

        if self.res.type != 'SineResource':
            raise ConfigurationError("SetSineResourceProperties: Resource '%s' is not a SineResource" % (self.resource))
            

        self.period = self.experiment.config.getfloat(self.config_section, 'period')
        if self.period and self.period <= 0:
            raise ConfigurationError("SetSineResourceProperties: Invalid value for period '%f'.  Must be nonzero and nonnegative." % (self.period))

        self.amplitude = self.experiment.config.getfloat(self.config_section, 'amplitude')
        if self.amplitude and self.amplitude < 0:
            raise ConfigurationError("SetSineResourceProperties: Invalid value for amplitude '%f'.  Must be nonnegative." % (self.amplitude))

        self.cells_str = self.experiment.config.get(self.config_section, 'cells')

        if not self.cells_str:
            self.cells = self.res.topology.graph.nodes()
        else:
            self.cells = parse_int_rangelist(self.cells_str, sorted=True)
            nids = self.res.topology.graph.nodes()
            for c in self.cells:
                if c not in nids:
                    raise ConfigurationError("SetSineResourceProperties: Cell %d does not exist in Resource '%s'" % (c, self.resource))

    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        for c in self.cells:
            if self.period:
                self.res.topology.graph.node[c]['resource'].period = self.period
            if self.amplitude:
                self.res.topology.graph.node[c]['resource'].amplitude = self.amplitude
