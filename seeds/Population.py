# -*- coding: utf-8 -*-
""" A population stores information related to the organisms that exist in an
experiment, including the graph that defines their interactions and a
dictionary to store any additional information about the population as a whole.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import random

from seeds.Experiment import *
from seeds.SEEDSError import *
from seeds.Topology import *


class Population(object):
    """Manage populations of organisms

    Properties:

    data
        A dict that can be used to store additional data about a population.
        For example, see the 'type_count' value, which is used to store the
        counts of different cell types (for cells that have different types)
        across the population.  This is faster than scanning the population
        whenever this information is needed.
    experiment
        A reference to the Experiment in which this Population exists
    topology
        A graph representing the organisms (nodes) and the potential
        interactions between them (edges)
    _cell_class
        A reference to the proper class for the configured Cell type

    """

    def __init__(self, experiment):
        self.experiment = experiment
        self.data = {}
        self.data['type_count'] = []

        # Create a topology to represent the organisms and their interactions
        pop_topology_type = self.experiment.config.get('Experiment', 'topology')
        try:
            tref = self.experiment.plugin_manager.get_plugin(pop_topology_type,
                                                             type=Topology)
            self.topology = tref(self.experiment)
        except PluginNotFoundError as err:
            raise TopologyPluginNotFoundError(pop_topology_type)

        # Create a reference for the configured Cell type
        cell_type = self.experiment.config.get('Experiment', 'cell')
        try:
            self._cell_class = self.experiment.plugin_manager.get_plugin(cell_type,
                                                                         type=Cell)
        except PluginNotFoundError as err:
            raise CellPluginNotFoundError(cell_type)

        # For each node in the topology, create a Cell and assign it the
        # coordinates of the node
        for n in self.topology.graph.nodes():
            c = self._cell_class(experiment=self.experiment, population=self,
                                 id=n)
            self.topology.graph.node[n]['cell'] = c

    def update(self):
        """Update the Population: update the topology stochastically

        During each update, a number of nodes in the topology are selected at
        random, and the update method of the Cells in the selected nodes is
        called.  By default, the number of nodes selected is equal to the
        number of nodes in the topology (so each node's Cell will be updated,
        on average, each epoch.  This number can be changed by setting the
        events_per_epoch parameter in the Experiment section of the
        configuration.
        
        """

        for x in xrange(self.experiment.config.getint(section='Experiment',
                                                      name='events_per_epoch',
                                                      default=len(self.topology.graph))):
            node = random.choice(self.topology.graph.nodes())
            self.topology.graph.node[node]['cell'].update()

    def teardown(self):
        """Perform teardown at the end of an experiment"""
        self.topology.teardown()

    def increment_type_count(self, type):
        """Increment the cell type count for the given type

        Parameters:

        *type*
            The cell type whose count to increment

        """

        if len(self.data['type_count']) <= type:
            self.data['type_count'].extend([0] * (1 + type-len(self.data['type_count'])))
        self.data['type_count'][type] += 1

    def decrement_type_count(self, type):
        """Decrement the cell type count for the given type

        Parameters:

        *type*
            cell type whose count to decrement

        """

        self.data['type_count'][type] -= 1

    def update_type_count(self, fromtype, totype):
        """Update the cell type counts, subtracting from the 'from' type and
        adding to the 'to' type

        Parameters:

        *fromtype*
            type that a cell was prior to being updated
        totype*
            type that a cell is after being updated

        """

        self.decrement_type_count(fromtype)
        self.increment_type_count(totype)

    def add_cell(self, neighbors=[]):
        """Add a Cell of the appropriate type to the population and connect it
        to the given neighbors (optional).

        Parameters:

        *neighbors*
            List of Cells to be connected to the newly-created Cell

        """

        neighbor_ids = []
        [neighbor_ids.append(n.id) for n in neighbors]

        new_id = max(self.topology.graph.nodes()) + 1

        try:
            self.topology.add_node(id=new_id, neighbors=neighbor_ids)
        except NonExistentNodeError as err:
            print "Error adding Cell: %s" % (err)

        c = self._cell_class(experiment=self.experiment, population=self,
                             id=new_id)

        self.topology.graph.node[n]['cell'] = c

