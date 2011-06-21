# -*- coding: utf-8 -*-
"""
Write a snapshot of the population
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.Action import *


class WriteSnapshot(Action):
    """ Write a Snapshot file

        Config file settings:
        [WriteSnapshot]
        epoch_start = 3    Epoch at which to start writing (default 0)
        epoch_end = 100    Epoch at which to stop writing (default end of experiment)
        frequency = 2      Frequency (epochs) to write.  In this example, we write every other epoch.  (default 1)
        priority = 0       Priority of this Action.  Higher priority Actions run first. (default 0)
        filename = snapshot  Base filename to be written to (will be <filename>-<epoch>.snp)
        write_on_end = True Whether or not to write a snapshot file at the end of a run, regardless of when that occurs

    """

    def __init__(self, experiment):
        """Initialize the WriteSnapshot Action"""

        super(WriteSnapshot, self).__init__(experiment)
        self.epoch_start = self.experiment.config.getint('WriteSnapshot', 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint('WriteSnapshot', 'epoch_end', default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint('WriteSnapshot', 'frequency', 1)
        self.priority = self.experiment.config.getint('WriteSnapshot', 'priority', 0)
        self.filename = self.experiment.config.get('WriteSnapshot', 'filename', 'snapshot')
        self.write_on_end = self.experiment.config.getboolean('WriteSnapshot', 'write_on_end', default=True)
        self.name = "WriteSnapshot"

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        data_file = self.datafile_path(self.filename)
        self.experiment.get_snapshot().write(data_file)

    def teardown(self):
        """Perform cleanup.  If user requests a snapshot to be written at the
        end of an experiment, do so.  This is useful if the experiment ends
        before a predefined number of epochs, as would be the case with Actions
        such as StopOnConvergence

        """

        if self.write_on_end:
            data_file = self.datafile_path(self.filename)
            self.experiment.get_snapshot().write(data_file)


class TESTSnapshot(Action):
    """ TODO doc

        Config file settings:
        [WriteSnapshot]
        epoch_start = 3    Epoch at which to start writing (default 0)
        epoch_end = 100    Epoch at which to stop writing (default end of experiment)
        frequency = 2      Frequency (epochs) to write.  In this example, we write every other epoch.  (default 1)
        filename = snapshot  Base filename to be written to (will be <filename>-<epoch>.snp)

    """

    def __init__(self, experiment):
        """Initialize the WriteSnapshot Action"""

        super(TESTSnapshot, self).__init__(experiment)
        self.epoch_start = self.experiment.config.getint('WriteSnapshot', 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint('WriteSnapshot', 'epoch_end', default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint('WriteSnapshot', 'frequency', 1)
        self.priority = self.experiment.config.getint('WriteSnapshot', 'priority', 0)
        self.filename = self.experiment.config.get('WriteSnapshot', 'filename', 'snapshot')
        self.name = "WriteSnapshot"

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        data_file = self.datafile_path(self.filename)
        self.experiment.get_snapshot().write(data_file)

    def teardown(self):
        if self.write_on_end:
            data_file = self.datafile_path(self.filename)
            self.experiment.get_snapshot().write(data_file)
