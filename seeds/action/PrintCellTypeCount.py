# -*- coding: utf-8 -*-
"""
Print the number of Cells for each cell type for all populations
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.2"
__credits__ = "Brian Connelly"


import csv

from seeds.Action import *

class PrintCellTypeCount(Action):
    """ Write the number of cells of each type for all populations

        Config file settings:
        [PrintCellTypeCount]
        epoch_start = 3    Epoch at which to start writing (default 0)
        epoch_end = 100    Epoch at which to stop writing (default end of experiment)
        frequency = 2      Frequency (epochs) to write.  In this example, we write every other epoch.  (default 1)
        filename = cell_type_count.dat  Filename to be written to

    """

    def __init__(self, world):
        """Initialize the PrintCellTypeCount Action"""

        Action.__init__(self, world)
        self.epoch_start = self.world.config.getint('PrintCellTypeCount', 'epoch_start', 0)
        self.epoch_end = self.world.config.getint('PrintCellTypeCount', 'epoch_end', default=self.world.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.world.config.getint('PrintCellTypeCount', 'frequency', 1)
        self.filename = self.world.config.get('PrintCellTypeCount', 'filename', 'cell_type_count.dat')
        self.name = "PrintCellTypeCount"

        data_file = self.datafile_path(self.filename)
        self.writer = csv.writer(open(data_file, 'w'))

        c = self.world.topology_manager.topologies[0].cell_manager.newcell(-1,-1)
        self.types = c.types
        self.world.topology_manager.topologies[0].decrement_type_count(c.type)
        c = None

        header = ['#epoch', 'population']
        header += self.types
        self.writer.writerow(header)

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        for top in self.world.topology_manager.topologies:
            row = [self.world.epoch, top.id] + top.typeCount
            self.writer.writerow(row)

