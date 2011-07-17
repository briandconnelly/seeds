# -*- coding: utf-8 -*-
"""
Print the number of Cells for each cell type
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


import csv

from seeds.Action import *

class PrintCellTypeCount(Action):
    """ Write the number of cells of each type

    Configuration is done in the [PrintCellTypeCount] section

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
        The name of the file to write to (default: cell_type_count.csv)
    header
        Whether or not to write a header to the output file.  The header will
        be an uncommented, comma-separated list of property names corresponding
        to the data in each row. (default: True)


    Configuration Example:

    [PrintCellTypeCount]
    epoch_start = 3
    epoch_end = 100
    frequency = 2
    priority = 0
    filename = cell_type_count.csv
    header = True

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

        self.types = self.experiment.population._cell_class.types

        data_file = self.datafile_path(self.filename)
        self.writer = csv.writer(open(data_file, 'w'))

        if self.header:
            header = ['epoch']
            header += self.types
            self.writer.writerow(header)

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        row = [self.experiment.epoch] + self.experiment.data['population']['type_count']
        self.writer.writerow(row)

