# -*- coding: utf-8 -*-
""" The Experiment encompasses all aspects of the experiment. It maintains the
Actions, Resources, Cells, the configuration, and time.

The state of the Experiment can be saved or loaded using Snapshots.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import os
import random
import sys
import time
import uuid

import seeds
from seeds.ActionManager import *
from seeds.Cell import *
from seeds.Config import *
from seeds.PluginManager import *
from seeds.Population import *
from seeds.SEEDSError import *
from seeds.Snapshot import *
from seeds.Topology import *

class Experiment(object):
    """
    The Experiment object captures the state of a experiment

    Properties:

    action_manager
        An ActionManager object which manages all Actions in the experiment
    config
        A Config object storing the configuration for the experiment
    epoch
        An integer storing the current epoch (unit of time)
    plugin_manager
        A PluginManager object which manages all Plugins for the experiment
    population
        A Population object that keeps information about the Cells (organisms)
        and their interactions
    proceed
        Boolean value indicating whether or not the experiment should continue.
    resources
        List of Resource objects available
    uuid
        A practically unique identifier for the experiment. (RFC 4122 ver 4)
    _cell_class
        A reference to the proper class for the configured Cell type
    _population_topology_class
        A reference to the proper class for the configured population Topology

    """

    def __init__(self, configfile=None, seed=-1):
        """Initialize a Experiment object

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

        self.config = Config(experiment=self, filename=configfile)
        self.epoch = 0
        self.is_setup = False
        self.proceed = True
        self.resources = []
        self.seed = seed
        self.uuid = uuid.uuid4()

    def setup(self):
        """Set up the Experiment including its Actions, Topologies, and Cells"""
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
        for d in ["cell", "topology", "action", "resource"]:
            plugin_path = os.path.join(global_plugin_path, d)
            self.plugin_manager.append_dir(plugin_path)

        # Create a reference for the configured Cell type
        cell_type = self.config.get('Experiment', 'cell')
        try:
            self._cell_class = self.plugin_manager.get_plugin(cell_type, type=Cell)
        except PluginNotFoundError as err:
            raise CellPluginNotFoundError(cell_type)

        # Create a reference for the configured population Topology type
        pop_topology_type = self.config.get('Experiment', 'topology')
        try:
            self._population_topology_class = self.plugin_manager.get_plugin(pop_topology_type, type=Topology)
        except PluginNotFoundError as err:
            raise TopologyPluginNotFoundError(pop_topology_type)

        self.population = Population(experiment=self)
        self.action_manager = ActionManager(experiment=self)

        self.is_setup = True

    def update(self):
        """Update the Experiment and all of its objects"""
        if not self.is_setup:
            self.setup()

        self.action_manager.update()	# Update the actions
        [r.update() for r in self.resources]
        self.population.update()
        self.epoch += 1

        # If we've surpassed the configured number of epochs to run for, set
        # proceed to false
        if self.experiment_epochs != -1 and self.epoch >= self.experiment_epochs:
            self.proceed = False

    def __iter__(self):
        """Experiment is an iterator, so it can be used with commands such as

        e = Experiment(....)
        for epoch in e:
            print "Updated Experiment.  Now at epoch %d" % (epoch)
        """

        return self

    def next(self):
        """Proceed with the experiment.  Update the Experiment and return the current epoch"""
        if not self.proceed:
            raise StopIteration
        else:
            self.update()
            return self.epoch

    def end(self):
        """Set the experiment to end after this epoch"""
        self.proceed = False

    def teardown(self):
        """Perform any necessary cleanup at the end of a run"""
        self.action_manager.teardown()
        [r.teardown() for r in self.resources]
        self.population.teardown()

    def create_cell(self, population, node, id):
        c = self._cell_class(self, population, node, id)
        return c

    def get_snapshot(self):
        """Get a Snapshot containing the state of the Experiment"""
        s = Snapshot()
        s.update(self)
        return s

    def load_snapshot(self, filename):
        """Load a Snapshot from file and set the state of the Experiment

        Parameters:

        *filename*
            The file from which to load the Snapshot

        """

        print "NOTICE: Loading snapshots is currently not working!"

        s = Snapshot() 
        s.read(filename)
        s.apply(self)

