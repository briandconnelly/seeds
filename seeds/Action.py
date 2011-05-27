# -*- coding: utf-8 -*-
"""
Interface for Actions.

An Action is a piece of code that is executed at specified epochs and perform
things such as writing statistics, plotting graphs, or interacting with
Topologies, Cells, or Resources.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly, Luis Zaman"

import os


class Action(object):
    """
    Properties:

    experiment
        A reference to the Experiment
    data_dir
        Directory in which to store created files
    epoch_start
        The epoch at which the Action starts executing
    epoch_end
        The epoch at which the Action stops executing
    frequency
        The frequency at which the Action is executed.  For example, if
        frequency=2, then the Action is executed at every other epoch.
    name
        The name of the action
    priority
        The priority of the action.  This is useful for actions for which it is
        important to execute in a specific order.  Larger values mean higher
        priority.  Default: 0.
    enabled
        Whether or not the Action should be run.  (Boolean, Default: True)
    
    Configuration: The data_dir parameter should be set in the [Experiment]
    block.  Each Action should have its own configuration block.

    """

    def __init__(self, experiment):
        """Create an Action instance"""
        self.experiment = experiment
        self.data_dir = self.experiment.config.get('Experiment', 'data_dir', 'data')
        self.epoch_start = 0
        self.epoch_end = self.experiment.config.getint('Experiment', 'epochs', default=-1)
        self.frequency = 1
        self.priority = 0
        self.name = ""
        self.enabled = True

    def __str__(self):
        """Produce a string to be used when an Action object is printed"""
        return 'Action Object (%s) (epoch start: %d)(epoch end: %d)(frequency: %d)' % (self.name, self.epoch_start, self.epoch_end, self.frequency)

    def update(self):
        """ Execute the action """
        pass

    def teardown(self):
        """Perform any necessary cleanup at the end of the experiment"""
        pass

    def skip_update(self):
        """ Return a boolean indicating whether or not the action should be
        executed during the current epoch

        """

        return (self.experiment.epoch < self.epoch_start or
                (self.epoch_end != -1 and self.experiment.epoch > self.epoch_end) or
                (self.experiment.epoch - self.epoch_start) % self.frequency != 0 or
                not self.enabled)

    def datafile_path(self, filename):
        """ Return the relative path to a given data file
        Parameters:

        *filename*
            The name of the file whose path to get

        """
        return os.path.join(self.data_dir, filename)

