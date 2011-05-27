# -*- coding: utf-8 -*-
"""
Print the coordinates of each cell and its type for each populaton
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

    """
    def __init__(self, world):
        """Initialize the PrintCellLocations Action"""
        super(PrintCellLocations, self).__init__(world)

        self.epoch_start = self.world.config.getint('PrintCellLocations', 'epoch_start', 0)
        self.epoch_end = self.world.config.getint('PrintCellLocations', 'epoch_end',
                                                  default=self.world.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.world.config.getint('PrintCellLocations', 'frequency', 1)
        self.priority = self.world.config.getint('PrintCellLocations', 'priority', 0)
        self.filename = self.world.config.get('PrintCellLocations', 'filename', 'cell_locations')
        self.name = "PrintCellLocations"

    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        filename = "%s-%06d.csv" % (self.filename, self.world.epoch)
        data_file = self.datafile_path(filename)
        header = ['epoch','population','cell_id','x','y','type']
        self.writer = csv.DictWriter(open(data_file, 'w'), header)
        self.writer.writeheader()

        for pop in self.world.populations:
            for n in pop.graph.nodes():
                cell = pop.graph.node[n]['cell']
                row = dict(epoch=self.world.epoch, population=pop.id,
                           cell_id=cell.id, x=cell.coords[0],
                           y=cell.coords[1], type=cell.type)
                self.writer.writerow(row)

