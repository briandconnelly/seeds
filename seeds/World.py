# -*- coding: utf-8 -*-
"""
The World encompasses all aspects of the experiment. It maintains the actions,
the topologies (Cells), the configuration, and time.

The state of the World can be saved or loaded using Snapshots.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import os
import random
import time
import uuid

import seeds
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
    uuid
        A practically unique identifier for the experiment. (RFC 4122 ver 4)

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

        self.uuid = uuid.uuid4()
        self.config = Config(world=self, filename=configfile)
        self.epoch = 0
        self.proceed = True
        self.seed = seed
        self.is_setup = False

    def setup(self):
        """Set up the World including its Actions, Topologies, and Cells"""
        if self.seed == -1:
            configseed = self.config.getint('Experiment', 'seed', default=-1)
            if configseed != -1:
                self.seed = configseed
            else:
                self.seed = int(time.time()*10)

        random.seed(self.seed)
        self.config.set('Experiment', 'seed', self.seed)

        self.experiment_epochs = self.config.getint('Experiment', 'epochs',
                                                    default=-1)

        # Create a plugin manager.  Append the system-wide plugins
        # to the list of plugin sources.
        self.plugin_manager = PluginManager(self)
        global_plugin_path = os.path.join(os.path.dirname(seeds.__file__), "plugins")
        for d in ["cell", "topology", "action"]:
            plugin_path = os.path.join(global_plugin_path, d)
            self.plugin_manager.append_dir(plugin_path)

        self.topology_manager = TopologyManager(self)
        self.action_manager = ActionManager(self)


        self.is_setup = True

    def update(self):
        """Update the World and all of its objects"""
        if not self.is_setup:
            self.setup()

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

        print "NOTICE: Loading snapshots is currently not working!"

        s = Snapshot() 
        s.read(filename)
        s.apply(self)

