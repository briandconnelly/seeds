# -*- coding: utf-8 -*-
"""
Stop the experiment when the number of existing Cell types drops below a
threshold in all populations.  This allows experiments to end earlier
than the configured number if epochs have passed or experiments to not
specify the total number of epochs to observe.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.2"
__credits__ = "Brian Connelly"

import csv

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

    """
    def __init__(self, world):
        """Initialize the StopOnConvergence Action"""
        Action.__init__(self, world)

        self.threshold = self.world.config.getint('StopOnConvergence', 'threshold', 0)
        self.epoch_start = self.world.config.getint('StopOnConvergence', 'epoch_start', 0)
        self.epoch_end = self.world.config.getint('StopOnConvergence', 'epoch_end',
                                                  default=self.world.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.world.config.getint('StopOnConvergence', 'frequency', 1)
        self.filename = self.world.config.get('StopOnConvergence', 'filename', 'cell_locations')
        self.name = "StopOnConvergence"

    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        converged = True

        for top in self.world.topology_manager.topologies:
            num_active_types = 0

            for tcount in top.typeCount:
                if tcount > 0:
                    num_active_types += 1

            if num_active_types >= self.threshold:
                converged = False

        if converged:
            self.world.end()

