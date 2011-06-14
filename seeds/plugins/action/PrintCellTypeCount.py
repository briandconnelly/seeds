# -*- coding: utf-8 -*-
"""
Print the number of Cells for each cell type for all populations
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
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
        priority = 0       Priority of this Action.  Higher priority Actions run first. (default 0)
        filename = cell_type_count.csv  Filename to be written to
        header = True       Whether or not to write a header row (default: true)

    """

    def __init__(self, experiment):
        """Initialize the PrintCellTypeCount Action"""

        super(PrintCellTypeCount, self).__init__(experiment)
        self.epoch_start = self.experiment.config.getint('PrintCellTypeCount', 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint('PrintCellTypeCount', 'epoch_end', default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint('PrintCellTypeCount', 'frequency', 1)
        self.priority = self.experiment.config.getint('PrintCellTypeCount', 'priority', 0)
        self.filename = self.experiment.config.get('PrintCellTypeCount', 'filename', 'cell_type_count.csv')
        self.header = self.experiment.config.getboolean('PrintCellTypeCount', 'header', default=True)
        self.name = "PrintCellTypeCount"

        self.types = self.experiment._cell_class.types

        header = ['epoch']
        header += self.types

        data_file = self.datafile_path(self.filename)
        self.writer = csv.DictWriter(open(data_file, 'w'), header)
        if self.header:
            self.writer.writeheader()

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        row = dict(epoch=self.experiment.epoch)
        for i in xrange(len(self.types)):
            row[self.types[i]] = self.experiment.population.data['type_count'][i]
        self.writer.writerow(row)

