# -*- coding: utf-8 -*-
""" Print a number of measures related to the graphs used for topologies

Note that this action may take considerable time to execute for large
topologies.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import networkx as nx

import csv

from seeds.Action import *
from seeds.utils.statistics import mean, std

class PrintPopulationGraphProperties(Action):
    """ Write various properties of the population topology graph

    Configuration is done in the [PrintPopulationGraphProperties] section

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
        The name of the file to write to (default:
        population_graph_properties.csv)
    header
        Whether or not to write a header to the output file.  The header will
        be an uncommented, comma-separated list of property names corresponding
        to the data in each row. (default: True)


    Configuration Example:

    [PrintPopulationGraphProperties]
    epoch_start = 3
    epoch_end = 100
    frequency = 2
    priority = 0
    filename = population_graph_properties.csv
    header = True

    """
    def __init__(self, experiment, label=None):
        """Initialize the PrintPopulationGraphProperties Action"""

        super(PrintPopulationGraphProperties, self).__init__(experiment,
                                                             name="PrintPopulationGraphProperties",
                                                             label=label)

        self.epoch_start = self.experiment.config.getint(self.config_section, 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint(self.config_section, 'epoch_end', default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint(self.config_section, 'frequency', 1)
        self.priority = self.experiment.config.getint(self.config_section, 'priority', 0)
        self.filename = self.experiment.config.get(self.config_section, 'filename', 'population_graph_properties.csv')
        self.header = self.experiment.config.get(self.config_section, 'header', default=True)

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
        degrees = list(nx.degree(g).values())
        row = [self.experiment.epoch, nx.number_of_nodes(g), nx.number_of_edges(g), mean(degrees), std(degrees), nx.average_clustering(g), nx.diameter(g), nx.number_connected_components(g)]
        self.writer.writerow(row)

