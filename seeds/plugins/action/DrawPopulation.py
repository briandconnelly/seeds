# -*- coding: utf-8 -*-

""" Draw the Population graph.  Nodes will be drawn with a color corresponding
to the type_colors property of the Cell type used.

NOTE: This action requires Matplotlib

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import csv

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError("DrawPopulation requires matplotlib")

import networkx as nx
from seeds.Action import *

class DrawPopulation(Action):
    """ Draw the Population graph

    Configuration parameters for this action are set in the
    [DrawPopulation] section.

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
        Base name for files.  The epoch at which the file was created and
        the extension (see format) will also comprise the resulting file
        name.  For example, a filename of 'population' when run at epoch
        1200 and using format pdf would produce the file
        population-001200.pdf.  (default: 'population')
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

    [DrawPopulation]
    epoch_start = 3
    epoch_end = 100
    frequency = 2
    priority = 0
    filename = population
    format = png
    transparent = True

    """
    def __init__(self, experiment, label=None):
        """Initialize the DrawPopulation Action"""

        super(DrawPopulation, self).__init__(experiment, name="DrawPopulation", label=label)

        self.epoch_start = self.experiment.config.getint(self.config_section, 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint(self.config_section, 'epoch_end',
                                                  default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint(self.config_section, 'frequency', 1)
        self.priority = self.experiment.config.getint(self.config_section, 'priority', 0)
        self.filename = self.experiment.config.get(self.config_section, 'filename', default='population')
        self.format = self.experiment.config.get(self.config_section, 'format', default='png')
        self.transparent = self.experiment.config.getboolean(self.config_section, 'transparent', default=False)
        self.display_epoch = self.experiment.config.getboolean(self.config_section, 'display_epoch', default=False)

        self.graph = self.experiment.population.topology.graph
        self.colors = self.experiment.population._cell_class.type_colors

        # Get the coordinates of each node
        self.pos = {}
        for n in self.graph.nodes():
            x = self.graph.node[n]['coords'][0]
            y = self.graph.node[n]['coords'][1]
            self.pos[n] = [x,y]

    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        # Get a list of the colors to use for each node
        cols = []
        for n in self.graph.nodes():
            cols.append(self.colors[self.graph.node[n]['cell'].type])

        plt.figure()
        nx.draw(self.graph, with_labels=False,
                pos=self.pos, edge_color='#777777', node_color=cols, node_size=40)

        if self.display_epoch:
            plt.text(0, -0.05, "Epoch: %d" % (self.experiment.epoch),
                     horizontalalignment='left',
                     size='small')

        filename = "%s-%06d.%s" % (self.filename, self.experiment.epoch, self.format)
        data_file = self.datafile_path(filename)
        plt.savefig(data_file, transparent=self.transparent)
        plt.close()
