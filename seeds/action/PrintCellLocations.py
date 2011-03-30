# -*- coding: utf-8 -*-
"""
Print the coordinates of each cell and its type for each populaton
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.2"
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
        filename = cell_locations Filename to be written to - note that a new file is created each time
                            this action is scheduled, so a value of "myfile" will create "myfile-00100.dat", etc.

    """
    def __init__(self, world):
        """Initialize the PrintCellLocations Action"""
        Action.__init__(self, world)

        self.epoch_start = self.world.config.getint('PrintCellLocations', 'epoch_start', 0)
        self.epoch_end = self.world.config.getint('PrintCellLocations', 'epoch_end',
                                                  default=self.world.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.world.config.getint('PrintCellLocations', 'frequency', 1)
        self.filename = self.world.config.get('PrintCellLocations', 'filename', 'cell_locations')
        self.name = "PrintCellLocations"

    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        filename = "%s-%06d.csv" % (self.filename, self.world.epoch)
        data_file = self.datafile_path(filename)
        self.writer = csv.writer(open(data_file, 'w'))

        self.writer.writerow(['#epoch','population','cell id','x','y','type'])

        for top in self.world.topology_manager.topologies:
            for n in top.graph.nodes():
                cell = top.graph.node[n]['cell']
                row = [self.world.epoch, top.id, cell.id, cell.coords[0], cell.coords[1], cell.type]
                self.writer.writerow(row)

