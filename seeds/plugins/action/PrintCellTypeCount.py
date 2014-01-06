# -*- coding: utf-8 -*-
"""
Print the number of Cells for each cell type
"""

__author__ = "Brian Connelly <bdc@bconnelly.net>"
__credits__ = "Brian Connelly"


import csv

from seeds.Action import *
from seeds.Plugin import *


class PrintCellTypeCount(Action, Plugin):
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

    __name__ = "PrintCellTypeCount"
    __version__ = (1,0)
    __author__ = "Brian Connelly <bdc@bconnelly.net>"
    __credits__ = "Brian Connelly"
    __description__ = "Print the number of Cells for each Cell type"
    __type__ = 4
    __requirements__ = []


    def __init__(self, experiment, label=None):
        """Initialize the PrintCellTypeCount Action"""

        super(PrintCellTypeCount, self).__init__(experiment,
                                                 name="PrintCellTypeCount",
                                                 label=label)

        self.epoch_start = self.experiment.config.getint(self.config_section, 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint(self.config_section, 'epoch_end', default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint(self.config_section, 'frequency', 1)
        self.priority = self.experiment.config.getint(self.config_section, 'priority', 0)
        self.filename = self.experiment.config.get(self.config_section, 'filename', 'cell_type_count.csv')
        self.header = self.experiment.config.getboolean(self.config_section, 'header', default=True)

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

