# -*- coding: utf-8 -*-
"""
Print the coordinates of each cell and its type for each world
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import csv

from seeds.Action import *

class PrintCellLocations(Action):
    """ Write the x,y coordinates of each cell and its type

        Config file settings:
        [PrintCellLocations]
        epoch_start = 3    Epoch at which to start writing (default 0)
        epoch_end = 100    Epoch at which to stop writing (default end of experiment)
        frequency = 2      Frequency (epochs) to write.  In this example, we write every other epoch.  (default 1)
        priority = 0       Priority of this Action.  Higher priority Actions run first. (default 0)
        filename = cell_locations Filename to be written to - note that a new file is created each time
                            this action is scheduled, so a value of "myfile" will create "myfile-00100.csv", etc.
        header = True       Whether or not to write a header row to output (default: true)

    """
    def __init__(self, experiment):
        """Initialize the PrintCellLocations Action"""
        super(PrintCellLocations, self).__init__(experiment)

        self.epoch_start = self.experiment.config.getint('PrintCellLocations', 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint('PrintCellLocations', 'epoch_end',
                                                  default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint('PrintCellLocations', 'frequency', 1)
        self.priority = self.experiment.config.getint('PrintCellLocations', 'priority', 0)
        self.filename = self.experiment.config.get('PrintCellLocations', 'filename', 'cell_locations')
        self.header = self.experiment.config.getboolean('PrintCellLocations', 'header', default=True)
        self.name = "PrintCellLocations"

    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        filename = "%s-%06d.csv" % (self.filename, self.experiment.epoch)
        data_file = self.datafile_path(filename)
        self.writer = csv.writer(open(data_file, 'w'))

        if self.header:
            header = ['epoch','cell_id','x','y','type']
            self.writer.writerow(header)

        g = self.experiment.population.topology.graph
        for n in g.nodes():
            cell = g.node[n]['cell']
            (xpos, ypos) = cell.coords()

            row = [self.experiment.epoch, cell.id, xpos, ypos, cell.type]
            self.writer.writerow(row)

