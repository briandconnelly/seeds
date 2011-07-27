# -*- coding: utf-8 -*-

""" The SetResourceAvailability action allows a resource to be made available
or unavailable.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.Action import *
from seeds.SEEDSError import *


class SetResourceAvailability(Action):
    """ Action to set the availability of a resource

    Configuration is done in the [SetResourceAvailability] section

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
    available
        Whether or not the resource is available.  Valid settings are
        'available', 'on', '1', 'yes', 'true', 'unavailable', 'off', '0', 'no',
        or 'false'.


    Configuration Example:

    [SetResourceAvailability]
    resource = glucose
    available = yes
    epoch_start = 0
    epoch_end = 100
    frequency = 1
    priority = 0

    """

    def __init__(self, experiment, label=None):
        """Initialize the SetResourceAvailability Action"""

        super(SetResourceAvailability, self).__init__(experiment,
                                                name="SetResourceAvailability",
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
            raise ConfigurationError("SetResourceAvailability: Resource '%s' is undefined" % (self.resource))

        self.available = self.experiment.config.get(self.config_section, 'available')

        if str(self.available).lower() in ['available', 'on', '1', 'yes', 'true']:
            self.val = True
        elif str(self.available).lower() in ['unavailable', 'off', '0', 'no', 'false']:
            self.val = False
        else:
            raise ConfigurationError("SetResourceAvailability: Invalid value for availability '%s'" % (self.available))


    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        self.res.available = self.val
