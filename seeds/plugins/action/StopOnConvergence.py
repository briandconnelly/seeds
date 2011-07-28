# -*- coding: utf-8 -*-
""" Stop the experiment when the number of existing Cell types in the
population drops below a threshold.  This allows experiments to end earlier
than the configured number if epochs have passed or experiments to not specify
the total number of epochs to observe.  This is accomplished by calling the
Experiment's end method.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.Action import *
from seeds.SEEDSError import *


class StopOnConvergence(Action):
    """ Stop the experiment when the number of exisiting cell types in the
    population drops below the configured threshold.

    Configuration is done in the [StopOnConvergence] section

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
    threshold
        The number of cell types at or below which to stop the experiment
        (default: 0)


    Configuration Example:

    [StopOnConvergence]
    threshold = 2
    epoch_start = 0
    epoch_end = 100
    frequency = 1
    priority = 0

    """

    def __init__(self, experiment, label=None):
        """Initialize the StopOnConvergence Action"""

        super(StopOnConvergence, self).__init__(experiment,
                                                name="StopOnConvergence",
                                                label=label)

        self.threshold = self.experiment.config.getint(self.config_section, 'threshold', 0)
        self.epoch_start = self.experiment.config.getint(self.config_section, 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint(self.config_section, 'epoch_end',
                                                  default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint(self.config_section, 'frequency', 1)
        self.priority = self.experiment.config.getint(self.config_section, 'priority', 0)

        if self.threshold < 0:
            raise ConfigurationError("StopOnConvergence: threshold value must be at least 0")

    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        converged = True

        num_active_types = 0
        for tcount in self.experiment.data['population']['type_count']:
            if tcount > 0:
                num_active_types += 1

        if num_active_types >= self.threshold:
            converged = False

        if converged:
            self.experiment.end()
