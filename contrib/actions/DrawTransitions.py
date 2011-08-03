# -*- coding: utf-8 -*-

""" Illustrate the transitions between cell types.  Nodes will be drawn with a
color corresponding to the type_colors property of the Cell type used.  A
directed edge between two nodes represents that the source node is losing (net)
cells to the destination node at that point in time.  The weight of the edge
represents the magnitude of this transfer.

NOTE: This action requires Matplotlib

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import csv
import math

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError("DrawTransitions requires matplotlib")

import networkx as nx
from seeds.Action import *

class DrawTransitions(Action):
    """ Draw the transitions between cell types

    Configuration parameters for this action are set in the
    [DrawTransitions] section.

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
        Base name for files.  The epoch at which the file was created and the
        extension (see format) will also comprise the resulting file name.  For
        example, a filename of 'transitions' when run at epoch 1200 and using
        format pdf would produce the file transitions-001200.pdf.  (default:
        'transitions')
    format
        The format to be used for resulting images.  Available formats
        depend on the particular installation of matplotlib, but often
        allow png, pdf, jpg, eps, and svg.  (default: 'png')
    transparent
        Whether or not the canvas (background of the image) will be
        transparent in the resulting images.  If not, the background will
        be white. (default: False)
    display_epoch
        Whether or not to include the epoch in text with the figure (default:
        False)

    Configuration Example:

    [DrawTransitions]
    epoch_start = 3
    epoch_end = 100
    frequency = 2
    priority = 0
    filename = population
    format = png
    transparent = True

    """
    def __init__(self, experiment, label=None):
        """Initialize the DrawTransitions Action"""

        super(DrawTransitions, self).__init__(experiment, name="DrawTransitions", label=label)

        self.epoch_start = self.experiment.config.getint(self.config_section, 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint(self.config_section, 'epoch_end',
                                                  default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint(self.config_section, 'frequency', 1)
        self.priority = self.experiment.config.getint(self.config_section, 'priority', 0)
        self.filename = self.experiment.config.get(self.config_section, 'filename', default='transitions')
        self.format = self.experiment.config.get(self.config_section, 'format', default='png')
        self.transparent = self.experiment.config.getboolean(self.config_section, 'transparent', default=False)
        self.display_epoch = self.experiment.config.getboolean(self.config_section, 'display_epoch', default=False)

        self.colors = self.experiment.population._cell_class.type_colors
        self.types = self.experiment.population._cell_class.types
        self.max_types = self.experiment.population._cell_class.max_types

        self.node_labels = {}

    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        edge_colors = []

        graph = nx.DiGraph()
        for i in range(self.max_types):
            graph.add_node(i)

        # Get a list of the sizes to use for each node
        node_sizes = []
        min_size = 10
        max_size = 35000

        # NOTE: this size is radius-based.  Do area-based for more accurate analogy?
        for i in range(self.max_types):
            count = float(self.experiment.data['population']['type_count'][i])
            frac = count / len(self.experiment.population.topology.graph)
            mysize = min_size + (frac * (max_size - min_size))
            node_sizes.append(mysize)

        if self.experiment.epoch > 0:
            # Get a list of the colors to use for each edge.
            edge_colors = []
            tmatrix = self.experiment.data['population']['transitions']

            for f in range(self.max_types):
                for t in range(self.max_types):
                    if tmatrix[f][t] > tmatrix[t][f]:
                        edge_colors.append(self.colors[f])
                        wt = tmatrix[f][t] - tmatrix[t][f]
                        graph.add_edge(f, t, weight=wt)

        # Make the figure
        plt.figure()
        nx.draw(graph, with_labels=False, pos=nx.circular_layout(graph),
                edge_color=edge_colors, node_color=self.colors, node_size=node_sizes, labels=self.node_labels)

        if self.display_epoch:
            plt.text(0, -0.05, "Epoch: %d" % (self.experiment.epoch),
                     horizontalalignment='left',
                     size='small')

        filename = "%s-%06d.%s" % (self.filename, self.experiment.epoch, self.format)
        data_file = self.datafile_path(filename)
        plt.savefig(data_file, transparent=self.transparent)
        plt.close()
