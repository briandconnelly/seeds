# -*- coding: utf-8 -*-

""" This template outlines the necessary components for implementing a new Action
in SEEDS.  Generally, this involves implementing a constructor (__init__) and
an update method.

Areas marked with 'TODO' should be replaced with code specific to the Action
being implemented.

The name of the Action type should be the name of the class.  The name of the
file should also match this.

Methods and parameters common to all Action objects can be seen in the
Action.py file in the main SEEDS codebase.  A good example Action would be the
PrintCellTypeCount action located in plugins/actions.

Once completed, new Action type files can be placed in a plugins directory and
used by appending the name of the Action to the "actions" parameter in the
[Experiment] section of the configuration file.

"""

__author__ = "TODO"
__credits__ = "TODO"


# TODO: if you'll be writing data files, you'll want to use the csv module.
# All data files created by SEEDS should be in csv format.
import csv

from seeds.Action import *

class TODO-ActionName(Action):
    """ TODO: add documentation for the action describing what it's done and
    how it's configured.
    """

    def __init__(self, experiment, label=None):
        """Initialize the Action"""

        # Call the Action constructor.  This will set various parameters common
        # to all actions, such as defining the self.config_section parameter,
        # used below.
        super(TODO-ActionName, self).__init__(experiment,
                                                 name="TODO-ActionName",
                                                 label=label)

        # TODO: all actions have the following configuration parameters
        self.epoch_start = self.experiment.config.getint(self.config_section, 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint(self.config_section, 'epoch_end', default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint(self.config_section, 'frequency', 1)
        self.priority = self.experiment.config.getint(self.config_section, 'priority', 0)

        # TODO: load and validate any other configuration parameters here

        # TODO: if you plan to have one output file for this action, create and
        # open it here.


    # TODO: the update method is called at each epoch and performs whatever
    # tasks are associated with the action (e.g., writing a row of data,
    # creating a plot, killing organisms, etc.).
    def update(self):
        """Execute the action"""

        # NOTE: this code can be kept here.  It allows actions to be run at
        # certain intervals by using the epoch_start, epoch_end, and frequency
        # parameters.
        if self.skip_update():
	        return

        # TODO: perform the tasks associated with this action.

