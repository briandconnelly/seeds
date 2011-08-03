# -*- coding: utf-8 -*-
"""Print statistics about the clusters of each Cell type and overall clustering
in the population.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import networkx as nx

import csv
import random

from seeds.Action import *
from seeds.utils.statistics import mean, std

class PrintPopulationTypeClusters(Action):
    """ Write a data file containing the numbers of clusters of each Cell type,
    as well as their mean size and the standard deviation in size

    Configuration is done in the [PrintPopulationTypeClusters] section

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
        population_type_clusters.csv)
    header
        Whether or not to write a header to the output file.  The header will
        be an uncommented, comma-separated list of property names corresponding
        to the data in each row. (default: True)


    Configuration Example:

    [PrintPopulationTypeClusters]
    epoch_start = 3
    epoch_end = 100
    frequency = 2
    priority = 0
    filename = population_type_clusters.csv
    header = True

    """
    def __init__(self, experiment, label=None):
        """Initialize the PrintPopulationTypeClusters Action"""

        super(PrintPopulationTypeClusters, self).__init__(experiment,
                                                          name="PrintPopulationTypeClusters",
                                                          label=label)

        self.epoch_start = self.experiment.config.getint(self.config_section, 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint(self.config_section, 'epoch_end', default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint(self.config_section, 'frequency', 1)
        self.priority = self.experiment.config.getint(self.config_section, 'priority', 0)
        self.filename = self.experiment.config.get(self.config_section, 'filename', 'population_type_clusters.csv')
        self.header = self.experiment.config.get(self.config_section, 'header', default=True)
        self.name = "PrintPopulationTypeClusters"
        self.types = self.experiment.population._cell_class.types

        data_file = self.datafile_path(self.filename)
        self.writer = csv.writer(open(data_file, 'w'))

        if self.header:
            header = ['epoch', 'total_clusters', 'total_size_mean', 'total_size_std']
            for t in self.types:
                header.append('%s_clusters' % (t))
                header.append('%s_size_mean' % (t))
                header.append('%s_size_std' % (t))
            self.writer.writerow(header)
      
    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        g = self.experiment.population.topology.graph
        cluster_counts = [0] * len(self.types)
        cluster_sizes = {}

        for i in range(len(self.types) + 1):
            cluster_sizes[i] = []

        unvisited = g.nodes()

        while len(unvisited) > 0:
            node = random.choice(unvisited)
            type = g.node[node]["cell"].type

            c = cluster(g, node)
            c_size = len(c)
            cluster_counts[type] += 1
            cluster_sizes[type].append(c_size)
            cluster_sizes[len(self.types)].append(c_size)

            [unvisited.remove(x) for x in c]

        row = [self.experiment.epoch]
        row.append(sum(cluster_counts))
        row.append(mean(cluster_sizes[len(self.types)]))
        row.append(std(cluster_sizes[len(self.types)]))

        for t in range(len(self.types)):
            row.append(cluster_counts[t])
            row.append(mean(cluster_sizes[t]))
            row.append(std(cluster_sizes[t]))

        self.writer.writerow(row)

def cluster(graph, node):
    visited_nodes = []

    def visit(node):
        visited_nodes.append(node)
        for n in graph.neighbors(node):
            if n not in visited_nodes and graph.node[n]['cell'].type == graph.node[node]['cell'].type:
                visit(n)

    visit(node)
    return visited_nodes

