# -*- coding: utf-8 -*-
""" Print basic statistics about the distribution of a Resource
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


import csv

from seeds.Action import *
from seeds.SEEDSError import *
from seeds.util import mean, std

class PrintResourceStats(Action):
    """ Write the number of cells of each type for all populations

        Config file settings:
        [PrintResourceStats]
        epoch_start = 3    Epoch at which to start writing (default 0)
        epoch_end = 100    Epoch at which to stop writing (default end of experiment)
        frequency = 2      Frequency (epochs) to write.  In this example, we write every other epoch.  (default 1)
        priority = 0       Priority of this Action.  Higher priority Actions run first. (default 0)
        filename = resource  Filename to be written to - note that the resource name will be appended to the file name,
                             so a value of 'res' when printing data for a resource named 'glucose' will write to a file
                             named 'res-glucose.csv'. (default: 'resource')
        header = True       Whether or not to write a header row (default: true)
        resource = glucose The name of the resource about which to print statistics

    """

    def __init__(self, experiment):
        """Initialize the PrintResourceStats Action"""

        super(PrintResourceStats, self).__init__(experiment)
        self.epoch_start = self.experiment.config.getint('PrintResourceStats', 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint('PrintResourceStats', 'epoch_end', default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint('PrintResourceStats', 'frequency', 1)
        self.priority = self.experiment.config.getint('PrintResourceStats', 'priority', 0)
        self.filename = self.experiment.config.get('PrintResourceStats', 'filename', 'resource')
        self.header = self.experiment.config.getboolean('PrintResourceStats', 'header', default=True)
        self.resource = self.experiment.config.get('PrintResourceStats', 'resource')
        self.name = "PrintResourceStats"

        self.res = self.experiment.resource_manager.get_resource(self.resource)

        full_filename = "%s-%s.csv" % (self.filename, self.resource)
        data_file = self.datafile_path(full_filename)
        self.writer = csv.writer(open(data_file, 'w'))

        if self.header:
            header = ['epoch','mean','standard_deviation']
            self.writer.writerow(header)

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        row = [self.experiment.epoch, mean(self.res.data['levels']),
               std(self.res.data['levels'])]
        self.writer.writerow(row)

