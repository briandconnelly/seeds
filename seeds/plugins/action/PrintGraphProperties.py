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

    """
    def __init__(self, world):
        """Initialize the PrintGraphProperties Action"""

        super(PrintGraphProperties, self).__init__(world)
        self.epoch_start = self.world.config.getint('PrintGraphProperties', 'epoch_start', 0)
        self.epoch_end = self.world.config.getint('PrintGraphProperties', 'epoch_end', default=self.world.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.world.config.getint('PrintGraphProperties', 'frequency', 1)
        self.priority = self.world.config.getint('PrintGraphProperties', 'priority', 0)
        self.filename = self.world.config.get('PrintGraphProperties', 'filename', 'graph_properties.csv')
        self.name = "PrintGraphProperties"

        data_file = self.datafile_path(self.filename)
        header = ['epoch', 'population', 'nodes', 'edges', 'avg_degree',
                  'std_degree', 'avg_clustering_coefficient','diameter',
                  'num_connected_components']
        self.writer = csv.DictWriter(open(data_file, 'w'), header)
        self.writer.writeheader()
      
    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        for pop in self.world.populations:
            degrees = nx.degree(pop.graph).values()
            row = dict(epoch=self.world.epoch, population=pop.id,
                       nodes=nx.number_of_nodes(pop.graph),
                       edges=nx.number_of_edges(pop.graph),
                       avg_degree=mean(degrees), std_degree=std(degrees),
                       avg_clustering_coefficient=nx.average_clustering(pop.graph),
                       diameter=nx.diameter(pop.graph),
                        num_connected_components=nx.number_connected_components(pop.graph))
            self.writer.writerow(row)

