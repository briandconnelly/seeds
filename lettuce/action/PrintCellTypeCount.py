"""
Print the number of Cells for each cell type across all populations
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "0.9.0"
__credits__ = "Brian Connelly"


import csv

from lettuce.Action import *

class PrintCellTypeCount(Action):
    """ Write the number of cells of each type in all populations

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
        self.epoch_end = self.world.config.getint('PrintCellTypeCount', 'epoch_end', self.world.config.getint('Experiment', 'epochs'))
        self.frequency = self.world.config.getint('PrintCellTypeCount', 'frequency', 1)
        self.filename = self.world.config.get('PrintCellTypeCount', 'filename', 'cell_type_count.dat')
        self.name = "PrintCellTypeCount"

        data_file = self.datafile_path(self.filename)
        self.writer = csv.writer(open(data_file, 'w'))

        self.types = self.world.topology_manager.topologies[0].cm.newcell(-1).types

        # Write a header containing the type names
        if len(self.types) > 0:
            header = self.types
            header[0] = "#%s" % (header[0])
            self.writer.writerow(header)

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        typeCountSum = []

        for top in self.world.topology_manager.topologies:
            if len(typeCountSum) == 0:
                typeCountSum = [0] * len(top.typeCount)

            if len(typeCountSum) != len(top.typeCount):
                # There is a chance these two lists may not be the same length.  Fix this.
                print 'FIXME'
            for i in xrange(len(typeCountSum)):
                typeCountSum[i] += top.typeCount[i]

        row = [self.world.epoch] + typeCountSum
        self.writer.writerow(row)

