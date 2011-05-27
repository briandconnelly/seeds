# -*- coding: utf-8 -*-
"""
Stop the experiment when the number of existing Cell types drops below a
threshold in all populations.  This allows experiments to end earlier
than the configured number if epochs have passed or experiments to not
specify the total number of epochs to observe.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.Action import *


class StopOnConvergence(Action):
    """ Stop the experiment when the number of exisiting cell types drops below
    the configured threshold in all populations

    Config file settings: All parameters for this action are specified in the
    [StopOnConvergence] configuration block.

    [StopOnConvergence]
    threshold = 3       Number of types below which the run will stop.
    epoch_start = 3     Epoch at which to start checking (default 0)
    epoch_end = 100     Epoch at which to stop checking (default end of experiment)
    frequency = 2       Frequency (epochs) to check the populations.  In this example, we write every other epoch.  (default 1)
    priority = 0        Priority of this Action.  Higher priority Actions run first. (default 0)

    """
    def __init__(self, experiment):
        """Initialize the StopOnConvergence Action"""
        super(StopOnConvergence, self).__init__(experiment)

        self.threshold = self.experiment.config.getint('StopOnConvergence', 'threshold', 0)
        self.epoch_start = self.experiment.config.getint('StopOnConvergence', 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint('StopOnConvergence', 'epoch_end',
                                                  default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint('StopOnConvergence', 'frequency', 1)
        self.priority = self.experiment.config.getint('StopOnConvergence', 'priority', 0)
        self.filename = self.experiment.config.get('StopOnConvergence', 'filename', 'cell_locations')
        self.name = "StopOnConvergence"

    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        converged = True

        for pop in self.experiment.populations:
            num_active_types = 0

            for tcount in pop.typeCount:
                if tcount > 0:
                    num_active_types += 1

            if num_active_types >= self.threshold:
                converged = False

        if converged:
            self.experiment.end()

