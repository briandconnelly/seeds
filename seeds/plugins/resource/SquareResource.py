# -*- coding: utf-8 -*-
"""
SquareResource represents a resource whose levels fluctuate between two
specific values.  These values and the fraction of time spent in either state
can be configured.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.Action import *
from seeds.ResourceCell import *
from seeds.SEEDSError import *
from seeds.utils.parsing import parse_int_rangelist


class SquareResource(ResourceCell):
    """Environmental Resource class

    Properties:

    id
        A unique ID for this node in the resource graph
    experiment
        A reference to the Experiment being performed
    resource
        A reference to the Resource of which this object is a part
    level
        The current level of the resource
    config_section
        The name of the section where parameters for this object are defined
    period
        period is the length of time (epochs) required to complete one cycle
        (integer values, units: epochs, default: 0).
    high
        high specifies the maximum value of the resource, which occurs in the
        high state (default: 0.0).
    low
        low specifies the minimum value of the resource, which occurs in the
        low state (default: 0.0).
    duty_cycle
        duty cycle is the fraction of one period that a resource spends in high
        state (default: 0.5).
    offset
        Offset defines the amount of time in epochs before the first high state
        is encountered (default: 0).

    SquareResource Resources can be defined in config files using a
    [Resource:<uniquename>] section and SquareResource type.  For example:

        [Resource:enzyme]
        type = SquareResource
        topology = CartesianTopology
        period = 100
        high = 5.8
        low = 0.0
        duty_cycle = 0.33
        offset = 5

    """

    def __init__(self, experiment, resource, config_section, id):
        """ Initialize a SquareResource object

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
        super(SquareResource, self).__init__(experiment=experiment,
                                             resource=resource,
                                             config_section=config_section,
                                             id=id)

        self.period = self.experiment.config.getint(self.config_section, "period", default=0)
        self.high = self.experiment.config.getfloat(self.config_section, "high", default=0.0)
        self.low = self.experiment.config.getfloat(self.config_section, "low", default=0.0)
        self.duty_cycle = self.experiment.config.getfloat(self.config_section, "duty_cycle", default=0.5)
        self.offset = self.experiment.config.getint(self.config_section, "offset", default=0)

        if self.period <= 0:
            raise ConfigurationError("SqureResource: period for '%s' must be greater than 0" % (self.resource.name))
        elif self.high < self.low:
            raise ConfigurationError("SqureResource: high vale for '%s' must be greater than low value" % (self.resource.name))
        elif self.duty_cycle < 0:
            raise ConfigurationError("SqureResource: duty cycle for '%s' must at least 0" % (self.resource.name))
        elif self.duty_cycle > 1:
            raise ConfigurationError("SqureResource: duty cycle for '%s' must be less than 1" % (self.resource.name))
        elif self.offset < 0:
            raise ConfigurationError("SqureResource: offset cycle for '%s' must at least 0" % (self.resource.name))

        # Set the initial level
        self.update()
        
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

        self.experiment.data['resources'][self.resource.name]['levels'][self.id] = self.level


class SetSquareResourceProperties(Action):
    """ Action to set the properties (period, high, low, or duty cycle) of a
    SquareResource resource

    Configuration is done in the [SetSquareResourceProperties] section

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
    high
        High specifies the maximum value of the resource, which occurs in the
        high state.  If no value is specified, the high value will not be
        altered.
    low
        Low specifies the minimum value of the resource, which occurs in the
        low state.  If no value is specified, the low value will not be
        altered.
    duty_cycle
        Duty cycle is the fraction of one period that a resource spends in high
        state.  If no value is specified, the duty cycle will not be altered.

    Configuration Example:

    [SetSquareResourceProperties]
    resource = glucose
    high = 10.2
    period = 100
    epoch_start = 0
    epoch_end = 100
    frequency = 1
    priority = 0

    """

    def __init__(self, experiment, label=None):
        """Initialize the SetSquareResourceProperties Action"""

        super(SetSquareResourceProperties, self).__init__(experiment,
                                                name="SetSquareResourceProperties",
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
            raise ConfigurationError("SetSquareResourceProperties: Resource '%s' is undefined" % (self.resource))

        if self.res.type != 'SquareResource':
            raise ConfigurationError("SetSquareResourceProperties: Resource '%s' is not a SquareResource" % (self.resource))
            

        self.period = self.experiment.config.getfloat(self.config_section, 'period')
        if self.period and self.period < 0:
            raise ConfigurationError("SetSquareResourceProperties: Invalid value for period '%f'.  Must be nonnegative." % (self.period))


        self.high = self.experiment.config.getfloat(self.config_section, 'high')
        self.low = self.experiment.config.getfloat(self.config_section, 'low')


        if self.high and self.low and self.high < self.low:
            raise ConfigurationError("SetSquareResourceProperties: High value must not be greater than low value." % (self.period))

        # NOTE: should also make sure that new high or low values (if one is not specified) is valid with the current configuration

        self.duty_cycle = self.experiment.config.getfloat(self.config_section, 'duty_cycle')
        if self.duty_cycle and self.duty_cycle < 0:
            raise ConfigurationError("SetSquareResourceProperties: Invalid value for duty_cycle '%f'.  Must be nonnegative." % (self.duty_cycle))

        if not self.period and not self.high and not self.low and not self.duty_cycle:
            raise ConfigurationError("SetSquareResourceProperties: Must specify value for period, high, low, or duty_cycle")

        self.cells_str = self.experiment.config.get(self.config_section, 'cells')

        if not self.cells_str:
            self.cells = self.res.topology.graph.nodes()
        else:
            self.cells = parse_int_rangelist(self.cells_str, sorted=True)
            nids = self.res.topology.graph.nodes()
            for c in self.cells:
                if c not in nids:
                    raise ConfigurationError("SetSquareResourceProperties: Cell %d does not exist in Resource '%s'" % (c, self.resource))

    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        for c in self.cells:
            if self.low:
                self.res.topology.graph.node[c]['resource'].low = self.low
            if self.high:
                self.res.topology.graph.node[c]['resource'].high = self.high
            if self.duty_cycle:
                self.res.topology.graph.node[c]['resource'].duty_cycle = self.duty_cycle
            if self.period:
                self.res.topology.graph.node[c]['resource'].period = self.period
