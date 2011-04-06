# -*- coding: utf-8 -*-
"""
Write a snapshot of the population
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


import csv

from seeds.Action import *

class WriteSnapshot(Action):
    """ Write the number of cells of each type for all populations

        Config file settings:
        [WriteSnapshot]
        epoch_start = 3    Epoch at which to start writing (default 0)
        epoch_end = 100    Epoch at which to stop writing (default end of experiment)
        frequency = 2      Frequency (epochs) to write.  In this example, we write every other epoch.  (default 1)
        filename = snapshot  Base filename to be written to (will be <filename>-<epoch>.snp)

    """

    def __init__(self, world):
        """Initialize the WriteSnapshot Action"""

        Action.__init__(self, world)
        self.epoch_start = self.world.config.getint('WriteSnapshot', 'epoch_start', 0)
        self.epoch_end = self.world.config.getint('WriteSnapshot', 'epoch_end', default=self.world.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.world.config.getint('WriteSnapshot', 'frequency', 1)
        self.filename = self.world.config.get('WriteSnapshot', 'filename', 'snapshot')
        self.name = "WriteSnapshot"

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        data_file = self.datafile_path(self.filename)
        self.world.get_snapshot().write(data_file)


class TESTSnapshot(Action):
    """ Write the number of cells of each type for all populations

        Config file settings:
        [WriteSnapshot]
        epoch_start = 3    Epoch at which to start writing (default 0)
        epoch_end = 100    Epoch at which to stop writing (default end of experiment)
        frequency = 2      Frequency (epochs) to write.  In this example, we write every other epoch.  (default 1)
        filename = snapshot  Base filename to be written to (will be <filename>-<epoch>.snp)

    """

    def __init__(self, world):
        """Initialize the WriteSnapshot Action"""

        Action.__init__(self, world)
        self.epoch_start = self.world.config.getint('WriteSnapshot', 'epoch_start', 0)
        self.epoch_end = self.world.config.getint('WriteSnapshot', 'epoch_end', default=self.world.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.world.config.getint('WriteSnapshot', 'frequency', 1)
        self.filename = self.world.config.get('WriteSnapshot', 'filename', 'snapshot')
        self.name = "WriteSnapshot"

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        data_file = self.datafile_path(self.filename)
        self.world.get_snapshot().write(data_file)
