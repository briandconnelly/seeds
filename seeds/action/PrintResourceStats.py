# -*- coding: utf-8 -*-
"""
Print information about the amount and distribution of resource present in each
population
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.2"
__credits__ = "Brian Connelly"

import csv

from seeds.Action import *


class PrintResourceStats(Action):
    """ Print information about the levels of resource present in each Topology

        Config file settings:
        [PrintResourceStats]
        epoch_start = 3     Epoch at which to start writing (default 0)
        epoch_end = 100     Epoch at which to stop writing (default end of experiment)
        frequency = 2       Frequency (epochs) to write.  In this example, we write every other epoch.  (default 1)
        resource = glucose  Name of resource
        filename = virulence.dat  Filename to be written to

    """

    def __init__(self, world):
        """Initialize the PrintResourceStats instance"""
        Action.__init__(self, world)

        self.epoch_start = self.world.config.getint('PrintResourceStats', 'epoch_start', 0)
        self.epoch_end = self.world.config.getint('PrintResourceStats', 'epoch_end', default=self.world.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.world.config.getint('PrintResourceStats', 'frequency', 1)
        self.resource = self.world.config.get('PrintResourceStats', 'resource')
        self.filename = self.world.config.get('PrintResourceStats', 'filename', 'resources.dat')

        data_file = self.datafile_path(self.filename)
        self.writer = csv.writer(open(data_file, 'w'))

        self.writer.writerow(['#epoch','population','mean resource level','std resource level'])

    def __str__(self):
        """Produce a string to be used when an object is printed"""
        return 'PrintResourceStats Object (epoch start: %d)(epoch end: %d)(frequency: %d)' % (self.epoch_start, self.epoch_end, self.frequency)

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        reslevels = []

        for top in self.world.topology_manager.topologies:
            for cell in top.cells:
                r = cell.resource_manager.get_resource(self.resource)
                if r != None:
                    reslevels.append(r.level)

            if len(reslevels) > 0:
                resmean = self.mean(reslevels)
                resstd = self.std(reslevels)
            else:
                resmean = 0
                resstd = 0

            row = [self.world.epoch] + [top.id, resmean, resstd]
            self.writer.writerow(row)

    def mean(self, data):
        """Calculate the mean of a list of numbers

        Parameters:

        *data*
            a list of numbers whose mean to calculate

        """

        return float(sum(data))/len(data)

    def std(self, data):
        """Calculate the standard deviation of a list of numbers

        Parameters:

        *data*
            a list of numbers whose standard deviation to calculate

        """
        m = self.mean(data)
        sumsq = 0

        for d in data:
            sumsq += (d - m)**2

        return (sumsq / len(data))**(0.5)

