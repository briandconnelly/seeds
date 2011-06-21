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
    """ Write information about the distribution of the given resource

    Configuration is done in the [PrintResourceStats] section

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
    filename
        The base name of the file to write to.  The name of the resource will
        be appended, so a filename of 'resource', when printing information
        about a resource named 'glucose', would produce the file
        'resource-glucost.csv'.  (default: resource)
    header
        Whether or not to write a header to the output file.  The header will
        be an uncommented, comma-separated list of property names corresponding
        to the data in each row. (default: True)
    resource
        The name of the resource about which to print information


    Configuration Example:

    [PrintResourceStats]
    epoch_start = 3
    epoch_end = 100
    frequency = 2
    priority = 0
    filename = resource
    header = True
    resource = glucose

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

