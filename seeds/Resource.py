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
    data
        A dict that can be used to store additional data about a population.
        This is faster than scanning the topology whenever this information is
        needed.
    experiment
        A reference to the Experiment in which the Resource exists
    name
        Unique name of the resource
    type
        The type of the resource (specific ResourceType class to be used)

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

    def __init__(self, experiment, name=None, available=True):
        """ Initialize a Resource object

        Parameters:

        *experiment*
            A pointer to the Experiment
        *name*
            A name for the resource
        *available*
            Whether or not the resource is currently available (default: True).
            When a resource is unavailable, get_level will return a level of
            0.0.

        """

        self.experiment = experiment
        self.data = {}

        if name != None:
            self.name = name
        else:
            print "Error: Must supply Resource name"

        self.config_section = "Resource:%s" % (name)
        self.available = available
        self.type = self.experiment.config.get(self.config_section, 'type',
                                               default='NormalResource')
        try:
            rtref = self.experiment.plugin_manager.get_plugin(self.type, type=ResourceType)
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

        # For each node in the topology, create a ResourceType object
        # TODO: get a reference for the resource type
        for n in self.topology.graph.nodes():
            self.topology.graph.node[n]['resource'] = rtref(experiment=self.experiment,
                                                            resource=self, 
                                                            config_section=self.config_section,
                                                            id=n)
            self.topology.graph.node[n]['resource'].coords = self.topology.graph.node[n]['coords']

        #TODO: now go through and grid the topology space creating the mapping for coordinates to node

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

