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
from seeds.ResourceType import *
from seeds.SEEDSError import *
from seeds.Topology import *


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
        The type of the resource (specific ResourceType class to be used)
    topology
        The Topology object that stores the graph of ResourceType (nodes)
        objects and the flow between them (edges)
    _resource_type_class
        A reference to the proper class for the configured ResourceType


    Resources are defined in config files using a [Resource:<uniquename>]
    section.  For example:

    [Resource:glucose}
    type = NormalResource
    initial = 10.0
    inflow = 1
    outflow = 0.1
    decay = 0.1

    For more information about the properties of this resource, see the
    documentation for NormalResource.

    """

    def __init__(self, experiment, name=None):
        """ Initialize a Resource object

        Parameters:

        *experiment*
            A pointer to the Experiment
        *name*
            A name for the resource

        """

        self.experiment = experiment

        if name != None:
            self.name = name
        else:
            print "Error: Must supply Resource name"

        self.experiment.data['resources'][name] = {}

        self.config_section = "Resource:%s" % (name)
        self.type = self.experiment.config.get(self.config_section, 'type',
                                               default='NormalResource')
        self.available = self.experiment.config.getboolean(self.config_section,
                                                           'available',
                                                           default=True)

        try:
            self._resource_type_class = self.experiment.plugin_manager.get_plugin(self.type, type=ResourceType)
        except PluginNotFoundError as err:
            raise ResourceTypePluginNotFoundError(self.type)

        topology_type = self.experiment.config.get(self.config_section, 'topology')
        try:
            tref = self.experiment.plugin_manager.get_plugin(topology_type, type=Topology)
        except PluginNotFoundError as err:
            raise TopologyPluginNotFoundError(topology_type)

        topology_secname = "%s:%s" % (self.name, topology_type)
        self.topology = tref(experiment=self.experiment,
                             config_section=topology_secname)

        self.experiment.data['resources'][name]['levels'] = [0] * self.topology.num_nodes()

        # For each node in the topology, create a ResourceType object
        for n in self.topology.graph.nodes():
            self.topology.graph.node[n]['resource'] = self._resource_type_class(experiment=self.experiment,
                                                                                resource=self, 
                                                                                config_section=self.config_section,
                                                                                id=n)

    def __str__(self):
        """Produce a string to be used when a Resource object is printed"""
        return "Resource [Name: %s][Topology: %s]" % (self.name, self.topology)

    def update(self):
        """Update the Resource

        During each update, a number of nodes in the topology are selected at
        random, and the update method of the ResourceType in the selected nodes
        is called.  By default, the number of nodes selected is equal to the
        number of nodes in the topology (so each node's ResourceType will be
        updated, on average, each epoch.  This number can be changed by setting
        the events_per_epoch parameter in the Experiment section of the
        configuration.
                                                                        
        """

        for x in xrange(self.experiment.config.getint(section='Experiment',
                                                      name='events_per_epoch',
                                                      default=len(self.topology.graph))):
            node = random.choice(self.topology.graph.nodes())
            self.topology.graph.node[node]['resource'].update()

    def teardown(self):
        """Perform any necessary cleanup at the end of the experiment"""
        self.topology.teardown()

    def add_resourcetype(self, rt=None, neighbors=[]):
        """Add a ResourceType of the appropriate type to the Resource and
        connect it to the given neighbors (optional).

        BDC: Does this method make sense?

        Parameters:

        *rt*
            An initialized ResourceType object to be used.  If this argument is
            not supplied, one will be created.
        *neighbors*
            List of ResourceTypes to be connected to the newly-created
            ResourceType

        """

        neighbor_ids = []
        [neighbor_ids.append(n.id) for n in neighbors]

        new_id = max(self.topology.graph.nodes()) + 1

        try:
            self.topology.add_node(id=new_id, neighbors=neighbor_ids)
        except NonExistentNodeError as err:
            print "Error adding ResourceType: %s" % (err)

        if not rt:
            rt = self._resource_type_class(experiment=self.experiment,
                                           resource=self,
                                           config_section=self.config_section,
                                           id=new_id)
 
        self.topology.graph.node[n]['resource'] = rt

    def remove_resourcetype(self, rt):
        """Remove the given ResourceType from the Resource and its
        corresponding interactions

        Parameters:

        *rt*
            The ResourceType object to be removed

        """

        try:
            self.topology.remove_node(cell.id)
        except NonExistentNodeError as err:
            print "Error removing ResourceType: %s" % (err)

    def connect_resourcetypes(self, src, dest):
        """Connect two ResourceType objects in the Population

        This creates an edge in the topology between the corresponding nodes.
        These ResourceTypes can then be considered neighbors and may
        potentially interact with one another.

        Note that if the two ResourceTypes are already connected, this will not
        create an additional connection.

        Parameters:

        src
            The first ResourceType to connect
        dest
            The second ResourceType to connect

        """

        try:
            self.topology.add_edge(src.id, dest.id)
        except NonExistentNodeError as err:
            print "Error connecting ResourceTypes: %s" % (err)

    def disconnect_resourcetypes(self, src, dest):
        """Disonnect two ResourceTypes in the Population

        This removes the edge in the topology between the corresponding nodes.
        These ResourceTypes are then no longer considered neighbors and will
        not interact with one another.

        Parameters:

        src
            The first ResourceType to disconnect
        dest
            The second ResourceType to disconnect

        """

        try:
            self.topology.remove_edge(src.id, dest.id)
        except NonExistentEdgeError as err:
            print "Error disconnecting ResourceTypes: %s" % (err)

    def resourcetpye_distance(self, src, dest):
        """Calculate the Cartesian distance between two ResourceTypes

        Properties:

        src
            The first ResourceTypes
        dest
            The second ResourceTypes

        """

        return self.topology.node_distance(src.id, dest.id)

