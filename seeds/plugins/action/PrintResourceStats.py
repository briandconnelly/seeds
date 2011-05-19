# -*- coding: utf-8 -*-
"""
Print information about the amount and distribution of resource present in each
population
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import csv

from seeds.Action import *
from seeds.util import mean, std


class PrintResourceStats(Action):
    """ Print information about the levels of resource present in each Topology

        Config file settings:
        [PrintResourceStats]
        epoch_start = 3     Epoch at which to start writing (default 0)
        epoch_end = 100     Epoch at which to stop writing (default end of experiment)
        frequency = 2       Frequency (epochs) to write.  In this example, we write every other epoch.  (default 1)
        priority = 0       Priority of this Action.  Higher priority Actions run first. (default 0)
        resource = glucose  Name of resource
        filename = resources.csv  Filename to be written to

    """

    def __init__(self, world):
        """Initialize the PrintResourceStats instance"""
        super(PrintResourceStats, self).__init__(world)
        self.name = "PrintResourceStats"

        self.epoch_start = self.world.config.getint('PrintResourceStats', 'epoch_start', 0)
        self.epoch_end = self.world.config.getint('PrintResourceStats', 'epoch_end', default=self.world.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.world.config.getint('PrintResourceStats', 'frequency', 1)
        self.priority = self.world.config.getint('PrintResourceStats', 'priority', 0)
        self.resource = self.world.config.get('PrintResourceStats', 'resource')
        self.filename = self.world.config.get('PrintResourceStats', 'filename', 'resources.csv')

        data_file = self.datafile_path(self.filename)
        header = ['epoch','population','mean_level','std_level']
        self.writer = csv.DictWriter(open(data_file, 'w'), header)
        self.writer.writeheader()

    def __str__(self):
        """Produce a string to be used when an object is printed"""
        return 'PrintResourceStats Object (epoch start: %d)(epoch end: %d)(frequency: %d)' % (self.epoch_start, self.epoch_end, self.frequency)

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return


        for top in self.world.topology_manager.topologies:
            reslevels = []

            for n in top.graph.nodes():
                r = top.graph.node[n]['resource_manager'].get_resource(self.resource)
                if r != None:
                    reslevels.append(r.level)

            if len(reslevels) > 0:
                resmean = mean(reslevels)
                resstd = std(reslevels)
            else:
                resmean = 0
                resstd = 0

            row = dict(epoch=self.world.epoch, population=top.id, mean_level=resmean, std_level=resstd)
            self.writer.writerow(row)

