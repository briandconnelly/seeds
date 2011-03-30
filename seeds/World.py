# -*- coding: utf-8 -*-
"""
The World encompasses all aspects of the experiment. It maintains the actions,
the topologies (Cells), the configuration, and time.

The state of the World can be saved or loaded using Snapshots.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.1"
__credits__ = "Brian Connelly"

import random
import time

from seeds.ActionManager import *
from seeds.Config import *
from seeds.PluginManager import *
from seeds.Snapshot import *
from seeds.TopologyManager import *

class World(object):
    """
    The World object captures the state of a experiment

    Properties:

    config
        A Config object storing the configuration for the experiment
    plugin_manager
        A PluginManager object which manages all Plugins for the experiment
    topology_manager
        A TopologyManager object which manages all Topologies in the experiment
    action_manager
        An ActionManager object which manages all Actions in the experiment
    epoch
        An integer storing the current epoch (unit of time)
    proceed
        Boolean value indicating whether or not the experiment should continue.

    """

    def __init__(self, configfile=None, seed=-1):
        """Initialize a World object

        Parameters:

        *configfile*
            Name of configuration file for the experiment.  If none is
            provided, the experiment will either use defaults for all
            parameters or values provided to the Config object elsewhere (e.g.,
            through the command-line or GUI program).
        *seed*
            Seed for pseudorandom number generator.  If undefined, the current
            time will be used.

        """

        self.config = Config(configfile)
        self.plugin_manager = PluginManager(self)
        self.topology_manager = TopologyManager(self)
        self.action_manager = ActionManager(self)
        self.epoch = 0
        self.proceed = True

        if seed == -1:
            configseed = self.config.getint('Experiment', 'seed', default=-1)
            if configseed != -1:
                seed = configseed
            else:
                seed = int(time.time()*10)

        random.seed(seed)
        self.config.set('Experiment', 'seed', seed)

        self.experiment_epochs = self.config.getint('Experiment', 'epochs',
                                                    default=-1)

    def update(self):
        """Update the World and all of its objects"""
        self.action_manager.update()	# Update the actions
        self.topology_manager.update()	# Update the topologies/cells
        self.epoch += 1

        # If we've surpassed the configured number of epochs to run for, set
        # proceed to false
        if self.experiment_epochs != -1 and self.epoch > self.experiment_epochs:
            self.proceed = False

    def end(self):
        """Set the experiment to end after this epoch"""
        self.proceed = False

    def get_snapshot(self):
        """Get a Snapshot containing the state of the World"""
        s = Snapshot()
        s.update(self)
        return s

    def load_snapshot(self, filename):
        """Load a Snapshot from file and set the state of the World

        Parameters:

        *filename*
            The file from which to load the Snapshot

        """

        s = Snapshot() 
        s.read(filename)
        s.apply(self)

