# -*- coding: utf-8 -*-
"""
The Experiment encompasses all aspects of the experiment. It maintains the
actions, the topologies (Cells), the configuration, and time.

The state of the Experiment can be saved or loaded using Snapshots.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import os
import random
import time
import uuid

import seeds
from seeds.ActionManager import *
from seeds.Cell import *
from seeds.Config import *
from seeds.PluginManager import *
from seeds.Snapshot import *
from seeds.Topology import *

class Experiment(object):
    """
    The Experiment object captures the state of a experiment

    Properties:

    config
        A Config object storing the configuration for the experiment
    plugin_manager
        A PluginManager object which manages all Plugins for the experiment
    populations
        A list of independent populations
    action_manager
        An ActionManager object which manages all Actions in the experiment
    epoch
        An integer storing the current epoch (unit of time)
    proceed
        Boolean value indicating whether or not the experiment should continue.
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

        self.uuid = uuid.uuid4()
        self.config = Config(experiment=self, filename=configfile)
        self.epoch = 0
        self.proceed = True
        self.seed = seed
        self.populations = []
        self.is_setup = False

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
        self._cell_class = self.plugin_manager.get_plugin(cell_type)
        if self._cell_class == None or not issubclass(self._cell_class, Cell):
            print "Error: Unknown Cell type '%s'" % (cell_type)

        # Create a reference for the configured population Topology type
        pop_topology_type = self.config.get('Experiment', 'topology')
        self._population_topology_class = self.plugin_manager.get_plugin(pop_topology_type)
        if self._population_topology_class == None or not issubclass(self._population_topology_class, Topology):
            print "Error: Unknown Topology type '%s'" % (pop_topology_type)

        # Create the populations
        for p in xrange(self.config.getint('Experiment', 'populations', default=1)):
            pop = self._population_topology_class(self, p)
            self.populations.append(pop)

        self.action_manager = ActionManager(self)

        self.is_setup = True

    def update(self):
        """Update the Experiment and all of its objects"""
        if not self.is_setup:
            self.setup()

        self.action_manager.update()	# Update the actions
        [pop.update() for pop in self.populations]
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
        [pop.teardown() for pop in self.populations]

    def create_cell(self, topology, node, id):
        c = self._cell_class(self, topology, node, id)
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

