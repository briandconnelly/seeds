# -*- coding: utf-8 -*-
"""
Print a number of measures related to the graphs used for topologies

Note that this action may take considerable time to execute for large
topologies.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.2"
__credits__ = "Brian Connelly"

import networkx as nx

import csv

from seeds.Action import *

class PrintGraphProperties(Action):
    """ Write various properties of the graphs used

        Config file settings:
        [PrintGraphProperties]
        epoch_start = 3    Epoch at which to start writing (default 0)
        epoch_end = 100    Epoch at which to stop writing (default end of experiment)
        frequency = 2      Frequency (epochs) to write.  In this example, we write every other epoch.  (default 1)
        filename = graph_properties.dat  Filename to be written to

    """
    def __init__(self, world):
        """Initialize the PrintGraphProperties Action"""
        Action.__init__(self, world)

        self.epoch_start = self.world.config.getint('PrintGraphProperties', 'epoch_start', 0)
        self.epoch_end = self.world.config.getint('PrintGraphProperties', 'epoch_end', default=self.world.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.world.config.getint('PrintGraphProperties', 'frequency', 1)
        self.filename = self.world.config.get('PrintGraphProperties', 'filename', 'graph_properties.dat')
        self.name = "PrintGraphProperties"

        data_file = self.datafile_path(self.filename)
        self.writer = csv.writer(open(data_file, 'w'))

        self.writer.writerow(['#epoch','population','nodes','edges','avg. degree', 'std. degree', 'avg. clustering coefficient','diameter', 'num connected components'])
      
    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        for top in self.world.topology_manager.topologies:
            degrees = nx.degree(top.graph).values()
            row = [self.world.epoch, top.id, nx.number_of_nodes(top.graph), nx.number_of_edges(top.graph), self.mean(degrees), self.std(degrees), nx.average_clustering(top.graph), nx.diameter(top.graph), nx.number_connected_components(top.graph)]
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

