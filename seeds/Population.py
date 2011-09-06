# -*- coding: utf-8 -*-
""" A population stores information related to the organisms that exist in an
experiment, including the graph that defines their interactions and a
dictionary to store any additional information about the population as a whole.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import itertools
import random

from seeds.Experiment import *
from seeds.SEEDSError import *
from seeds.Topology import *
from seeds.utils.sampling import sample_with_replacement


class Population(object):
    """Manage populations of organisms

    Properties:

    experiment
        A reference to the Experiment in which this Population exists
    topology
        A graph representing the organisms (nodes) and the potential
        interactions between them (edges)
    label
        A unique label specifying the configuration of the Population
    config_section
        A string containing the section under which this population is
        configured
    cell_id_manager
        Keeps track of Cell IDs and provides unique IDs using the get_cell_id
        method.
    _cell_class
        A reference to the proper class for the configured Cell type

    """

    def __init__(self, experiment, label=None):
        self.experiment = experiment
        self.label = label

        if self.label:
            self.config_section = "%s:%s" % ("Population", self.label)
        else:
            self.config_section = "%s" % ("Population")

        if not self.experiment.config.has_section(self.config_section):
            raise ConfigurationError("Configuration section %s not defined" % (self.config_section))

        self.cell_id_manager = itertools.count(0)

        self.experiment.data['population']['type_count'] = []
        self.experiment.data['population']['transitions'] = []

        # Create a topology to represent the organisms and their interactions
        pop_topology_raw = self.experiment.config.get(self.config_section, 'topology')
        parsed = pop_topology_raw.split(':')

        pop_topology_type = parsed[0]
        if len(parsed) > 1:
            label = parsed[1]
        else:
            label = None

        try:
            tref = self.experiment.plugin_manager.get_plugin(pop_topology_type,
                                                             type=Topology)
            self.topology = tref(self.experiment, label=label)
        except PluginNotFoundError as err:
            raise TopologyPluginNotFoundError(pop_topology_type)

        # Create a reference for the configured Cell type
        cell_config = self.experiment.config.get(self.config_section, 'cell')

        parsed = cell_config.split(':')
        cell_type = parsed[0]

        if len(parsed) > 1:
            label = parsed[1]
        else:
            label = None

        try:
            self._cell_class = self.experiment.plugin_manager.get_plugin(cell_type,
                                                                         type=Cell)
        except PluginNotFoundError as err:
            raise CellPluginNotFoundError(cell_type)

        # For each node in the topology, create a Cell and assign it the
        # coordinates of the node
        for n in self.topology.graph.nodes():
            c = self._cell_class(experiment=self.experiment, population=self,
                                 node=n, label=label)
            self.topology.graph.node[n]['cell'] = c

        # Now that all Cells are present, set their neighbors list.  This can
        # help speed updates up when the topology changes less than once per
        # epoch.  This benefit is most significant for fixed topologies.
        for n in self.topology.graph.nodes():
            self.topology.graph.node[n]['cell'].update_neighbors()

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

        # Reset the transitions count.  Long-term transitions data can be
        # obtained by using the PrintCellTypeTransitions action
        num_types = self._cell_class.max_types
        self.experiment.data['population']['transitions'] = [[0]*num_types for i in range(num_types)]

        # Select a set of cells to update and update them
        events = self.experiment.config.getint(section=self.config_section,
                                               name='events_per_epoch',
                                               default=len(self.topology.graph))
        nodes_to_update = sample_with_replacement(self.topology.graph.nodes(), k=events)
        [self.topology.graph.node[n]['cell'].update() for n in nodes_to_update]

    def teardown(self):
        """Perform teardown at the end of an experiment"""
        self.topology.teardown()

    def increment_type_count(self, type):
        """Increment the cell type count for the given type

        Parameters:

        *type*
            The cell type whose count to increment

        """

        if len(self.experiment.data['population']['type_count']) <= type:
            self.experiment.data['population']['type_count'].extend([0] * (1 + type-len(self.experiment.data['population']['type_count'])))
        self.experiment.data['population']['type_count'][type] += 1

    def decrement_type_count(self, type):
        """Decrement the cell type count for the given type

        Parameters:

        *type*
            cell type whose count to decrement

        """

        self.experiment.data['population']['type_count'][type] -= 1

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
        self.add_transition(fromtype, totype)

    def add_transition(self, fromtype, totype):
        """Update the transition counts

        Parameters:

        *fromtype*
            type that a cell was prior to being updated
        totype*
            type that a cell is after being updated

        """

        self.experiment.data['population']['transitions'][fromtype][totype] += 1

    def cell_distance(self, src, dest):
        """Calculate the Cartesian distance between two cells

        Properties:

        src
            The first cell
        dest
            The second cell

        """

        return self.topology.node_distance(src.id, dest.id)

    def add_cell(self, cell=None, neighbors=[], coords=None):
        """Add a Cell of the appropriate type to the population and connect it
        to the given neighbors (optional).

        Parameters:

        *cell*
            An initialized Cell object to be added
        *neighbors*
            List of Cells to be connected to the newly-created Cell
        *coords*
            A tuple containing the coordinates of the new cell.  The degree of
            this tuple must match the number of dimensions represented in the
            topology.  If none are supplied, the origin (0,..,0) will be used.

        """

        neighbor_ids = []
        [neighbor_ids.append(n.id) for n in neighbors]

        new_id = max(self.topology.graph.nodes()) + 1

        try:
            self.topology.add_node(id=new_id, neighbors=neighbor_ids, coords=coords)
        except NonExistentNodeError as err:
            # Perhaps a different exception would make more sense
            raise NonExistentNodeError(new_id)

        if not Cell:
            cell = self._cell_class(experiment=self.experiment,
                                    population=self, id=new_id)
        else:
            cell.id = new_id

        self.topology.graph.node[n]['cell'] = cell

    def remove_cell(self, cell):
        """Remove the given Cell from the Population and its corresponding
        interactions

        Parameters:

        *cell*
            The Cell object to be removed

        """

        try:
            self.topology.remove_node(cell.id)
        except NonExistentNodeError as err:
            print("Error removing Cell: %s" % (err))

    def connect_cells(self, src, dest):
        """Connect two Cells in the Population

        This creates an edge in the topology between the corresponding nodes.
        These Cells can then be considered neighbors and may potentially
        interact with one another.

        Note that if the two Cells are already connected, this will not create
        an additional connection.

        Parameters:

        src
            The first Cell to connect
        dest
            The second Cell to connect

        """

        try:
            self.topology.add_edge(src.id, dest.id)
        except NonExistentNodeError as err:
            print("Error connecting Cells: %s" % (err))

    def disconnect_cells(self, src, dest):
        """Disonnect two Cells in the Population

        This removes the edge in the topology between the corresponding nodes.
        These Cells are then no longer considered neighbors and will not
        interact with one another.

        Parameters:

        src
            The first Cell to disconnect
        dest
            The second Cell to disconnect

        """

        try:
            self.topology.remove_edge(src.id, dest.id)
        except NonExistentEdgeError as err:
            print("Error disconnecting Cells: %s" % (err))

    def get_cell_id(self):
        """Return a unique ID to be used for a Cell"""
        return self.cell_id_manager.next()

    def get_neighbors(self, cell):
        """Return a list of the neighbors for the given cell"""
        return [self.topology.graph.node[n]['cell'] for n in self.topology.get_neighbors(cell.node)]
