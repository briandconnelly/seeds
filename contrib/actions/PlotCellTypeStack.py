# -*- coding: utf-8 -*-
""" Create a stack plot displaying the abundances of each cell type in the
population over time.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy
import random

from seeds.Action import *

# Remove tick marks from plot axes
mpl.rcParams['xtick.major.size'] = 0
mpl.rcParams['xtick.minor.size'] = 0
mpl.rcParams['ytick.major.size'] = 0
mpl.rcParams['ytick.minor.size'] = 0


class PlotCellTypeStack(Action):
    """ TODO: description

    Configuration is done in the [PlotCellTypeStack] section

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
        The name of the resulting file (default: cell_type_stack.pdf)

    Configuration Example:

    [PlotCellTypeStack]
    epoch_start = 100
    frequency = 2
    priority = 0

    """

    def __init__(self, experiment, label=None):
        """Initialize the PlotCellTypeStack Action"""

        super(PlotCellTypeStack, self).__init__(experiment,
                                        name="PlotCellTypeStack",
                                        label=label)

        self.epoch_start = self.experiment.config.getint(self.config_section, 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint(self.config_section, 'epoch_end', default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint(self.config_section, 'frequency', 1)
        self.priority = self.experiment.config.getint(self.config_section, 'priority', 0)
        self.filename = self.experiment.config.get(self.config_section, 'filename', 'cell_type_stack.pdf')

        self.epochs = []
        self.typecounts = []

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        self.epochs.append(self.experiment.epoch)
        x = [i for i in self.experiment.data['population']['type_count']]
        self.typecounts.append(x)

    def teardown(self):
        """Since we're at the end of the run, plot the data"""

        if len(self.epochs) > 0 and len(self.typecounts) > 0:
            num_types = self.experiment.population._cell_class.max_types

            fig = plt.figure()
            plt.xlabel("Time (epoch)")
            plt.ylabel("Abundance (cells)")

            prev_xvals = [0] * len(self.epochs)
            for t in range(num_types):
                xvals = []
                for z in range(len(self.typecounts)):
                    xvals.append(self.typecounts[z][t] + prev_xvals[z])

                plt.fill_between(self.epochs, prev_xvals, xvals, color=self.experiment.population._cell_class.type_colors[t])
                prev_xvals = xvals

            end_epoch = self.experiment.config.getint('Experiment', 'epochs')
            if not end_epoch:
                end_epoch = max(self.epochs)

            plt.xlim([self.epoch_start, end_epoch])

            data_file = self.datafile_path(self.filename)
            plt.savefig(data_file)
