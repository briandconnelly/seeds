# -*- coding: utf-8 -*-
"""
Print a number of measures related to the graphs used for topologies

Note that this action may take considerable time to execute for large
topologies.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import networkx as nx

import csv

from seeds.Action import *
from seeds.util import mean, std

class PrintGraphProperties(Action):
    """ Write various properties of the graphs used

        Config file settings:
        [PrintGraphProperties]
        epoch_start = 3    Epoch at which to start writing (default 0)
        epoch_end = 100    Epoch at which to stop writing (default end of experiment)
        frequency = 2      Frequency (epochs) to write.  In this example, we write every other epoch.  (default 1)
        priority = 0       Priority of this Action.  Higher priority Actions run first. (default 0)
        filename = graph_properties.csv  Filename to be written to
        header = True       Whether or not to write a header row (default: True)

    """
    def __init__(self, experiment):
        """Initialize the PrintGraphProperties Action"""

        super(PrintGraphProperties, self).__init__(experiment)
        self.epoch_start = self.experiment.config.getint('PrintGraphProperties', 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint('PrintGraphProperties', 'epoch_end', default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint('PrintGraphProperties', 'frequency', 1)
        self.priority = self.experiment.config.getint('PrintGraphProperties', 'priority', 0)
        self.filename = self.experiment.config.get('PrintGraphProperties', 'filename', 'graph_properties.csv')
        self.header = self.experiment.config.get('PrintGraphProperties', 'header', default=True)
        self.name = "PrintGraphProperties"

        data_file = self.datafile_path(self.filename)
        self.writer = csv.writer(open(data_file, 'w'))

        if self.header:
            header = ['epoch', 'nodes', 'edges', 'avg_degree', 'std_degree',
                      'avg_clustering_coefficient','diameter',
                      'num_connected_components']
            self.writer.writerow(header)
      
    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        g = self.experiment.population.topology.graph
        degrees = nx.degree(g).values()
        row = [self.experiment.epoch, nx.number_of_nodes(g), nx.number_of_edges(g), mean(degrees), std(degrees), nx.average_clustering(g), nx.diameter(g), nx.number_connected_components(g)]
        self.writer.writerow(row)

