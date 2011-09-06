# -*- coding: utf-8 -*-
""" A Resource object represents the amount of a particular resource at a given
location in space.  Resources have a level that can be checked, consumed, or
added to.  Different Resource objects may have different objects such as inflow
and may interact with neighboring Resource objects (e.g., for diffusion).

This class provides the base properties and functionality for all Resources
used in SEEDS.  Specific implementations can be seen in plugins/resource.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.Experiment import *
from seeds.PluginManager import *
from seeds.ResourceCell import *
from seeds.SEEDSError import *
from seeds.Topology import *
from seeds.utils.sampling import sample_with_replacement


class Resource(object):
    """Interface for Resources

    Properties:

    available
        Whether or not the resource is currently available (default: True)
    experiment
        A reference to the Experiment in which the Resource exists
    name
        Unique name of the resource
    type
        The type of the resource (specific ResourceCell class to be used)
    topology
        The Topology object that stores the graph of ResourceCell (nodes)
        objects and the flow between them (edges)
    _resource_type_class
        A reference to the proper class for the configured ResourceCell


    Resources are defined in config files using a [Resource:<label>]
    section.  For example:

    [Resource:glucosev1}
    name = glucose
    type = NormalResource
    initial = 10.0
    inflow = 1
    outflow = 0.1
    decay = 0.1

    For more information about the properties of this resource, see the
    documentation for NormalResource.

    """

    def __init__(self, experiment, label=None):
        """ Initialize a Resource object

        Parameters:

        *experiment*
            A pointer to the Experiment
        *label*
            A label for a unique configuration of a resource.

        """

        self.experiment = experiment

        if label:
            self.label = label
        else:
            raise ConfigurationError("Must supply a Resource label")

        self.config_section = "Resource:%s" % (self.label)
        self.name = self.experiment.config.get(self.config_section, "name",
                                               default=self.label)

        self.experiment.data['resources'][self.name] = {}

        self.type = self.experiment.config.get(self.config_section, 'type',
                                               default='NormalResource')
        self.available = self.experiment.config.getboolean(self.config_section,
                                                           'available',
                                                           default=True)

        try:
            self._resource_type_class = self.experiment.plugin_manager.get_plugin(self.type, type=ResourceCell)
        except PluginNotFoundError as err:
            raise ResourceCellPluginNotFoundError(self.type)

        topology_raw = self.experiment.config.get(self.config_section, 'topology')
        parsed = topology_raw.split(':')

        topology_type = parsed[0]

        if len(parsed) > 1:
            top_label = parsed[1]
        else:
            top_label = None

        if topology_type != "MooreTopology" and topology_type != "VonNeumannTopology":
            raise ConfigurationError("SEEDS does not currently support Resource topology types other than MooreTopology or VonNeumannTopology")

        try:
            tref = self.experiment.plugin_manager.get_plugin(topology_type, type=Topology)
        except PluginNotFoundError as err:
            raise TopologyPluginNotFoundError(topology_type)

        self.topology = tref(experiment=self.experiment,
                             label=top_label)

        self.experiment.data['resources'][self.name]['levels'] = [0] * self.topology.num_nodes()

        # For each node in the topology, create a ResourceCell object
        for n in self.topology.graph.nodes():
            self.topology.graph.node[n]['resource'] = self._resource_type_class(experiment=self.experiment,
                                                                                resource=self, 
                                                                                config_section=self.config_section,
                                                                                id=n)

        # Now that all ResourceCells are present, set their neighbors list.
        # This can help speed updates up when the topology changes less than
        # once per epoch.  This benefit is most significant for fixed
        # topologies.
        for n in self.topology.graph.nodes():
            self.topology.graph.node[n]['resource'].update_neighbors()

    def __str__(self):
        """Produce a string to be used when a Resource object is printed"""
        return "Resource [Name: %s][Topology: %s]" % (self.name, self.topology)

    def update(self):
        """Update the Resource

        During each update, a number of nodes in the topology are selected at
        random, and the update method of the ResourceCell in the selected nodes
        is called.  By default, the number of nodes selected is equal to the
        number of nodes in the topology (so each node's ResourceCell will be
        updated, on average, each epoch.  This number can be changed by setting
        the events_per_epoch parameter in the Experiment section of the
        configuration.
                                                                        
        """

        events = self.experiment.config.getint(section=self.config_section,
                                               name='events_per_epoch',
                                               default=len(self.topology.graph))
        nodes_to_update = sample_with_replacement(self.topology.graph.nodes(), k=events)
        [self.topology.graph.node[n]['resource'].update() for n in nodes_to_update]

    def teardown(self):
        """Perform any necessary cleanup at the end of the experiment"""
        self.topology.teardown()

    def add_resourcetype(self, rt=None, neighbors=[]):
        """Add a ResourceCell of the appropriate type to the Resource and
        connect it to the given neighbors (optional).

        BDC: Does this method make sense?

        Parameters:

        *rt*
            An initialized ResourceCell object to be used.  If this argument is
            not supplied, one will be created.
        *neighbors*
            List of ResourceCells to be connected to the newly-created
            ResourceCell

        """

        neighbor_ids = []
        [neighbor_ids.append(n.id) for n in neighbors]

        new_id = max(self.topology.graph.nodes()) + 1

        try:
            self.topology.add_node(id=new_id, neighbors=neighbor_ids)
        except NonExistentNodeError as err:
            print("Error adding ResourceCell: %s" % (err))

        if not rt:
            rt = self._resource_type_class(experiment=self.experiment,
                                           resource=self,
                                           config_section=self.config_section,
                                           id=new_id)
 
        self.topology.graph.node[n]['resource'] = rt

    def remove_resourcetype(self, rt):
        """Remove the given ResourceCell from the Resource and its
        corresponding interactions

        Parameters:

        *rt*
            The ResourceCell object to be removed

        """

        try:
            self.topology.remove_node(cell.id)
        except NonExistentNodeError as err:
            print("Error removing ResourceCell: %s" % (err))

    def connect_resourcetypes(self, src, dest):
        """Connect two ResourceCell objects in the Population

        This creates an edge in the topology between the corresponding nodes.
        These ResourceCells can then be considered neighbors and may
        potentially interact with one another.

        Note that if the two ResourceCells are already connected, this will not
        create an additional connection.

        Parameters:

        src
            The first ResourceCell to connect
        dest
            The second ResourceCell to connect

        """

        try:
            self.topology.add_edge(src.id, dest.id)
        except NonExistentNodeError as err:
            print("Error connecting ResourceCells: %s" % (err))

    def disconnect_resourcetypes(self, src, dest):
        """Disonnect two ResourceCells in the Population

        This removes the edge in the topology between the corresponding nodes.
        These ResourceCells are then no longer considered neighbors and will
        not interact with one another.

        Parameters:

        src
            The first ResourceCell to disconnect
        dest
            The second ResourceCell to disconnect

        """

        try:
            self.topology.remove_edge(src.id, dest.id)
        except NonExistentEdgeError as err:
            print("Error disconnecting ResourceCells: %s" % (err))

    def resourcetpye_distance(self, src, dest):
        """Calculate the Cartesian distance between two ResourceCells

        Properties:

        src
            The first ResourceCell
        dest
            The second ResourceCell

        """

        return self.topology.node_distance(src.id, dest.id)
