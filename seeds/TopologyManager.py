# -*- coding: utf-8 -*-
"""
Manage Topology objects and initialize the right type based on the
configuration

If the configured Topology is not part of the standard SEEDS ones, the plugin
manager will be used to see if it has been defined by the user.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.2"
__credits__ = "Brian Connelly"

import seeds.topology
from seeds.topology import *

from seeds.PluginManager import *


class TopologyManager(object):
    """Manage the different Topology types and use the correct one

    Attributes:
        world
            A reference to the World object
        topologies
            A list of Topology objects

    """

    def __init__(self, world):
        """Initialize the TopologyManager

        Parameters:

        *world*
            A reference to the World

        """

        self.world = world
        self.topologies = []

        self.type = self.world.config.get('Experiment', 'topology')
        num_populations = self.world.config.getint('Experiment', 'populations', 1)

        for topid in xrange(num_populations):
            if self.type == 'Topology':
                t = Topology(self.world, topid)
            elif self.type == 'CartesianTopology':
                t = CartesianTopology(self.world, topid)
            elif self.type == 'MooreTopology':
                t = MooreTopology(self.world, topid)
            elif self.type == 'WellMixedTopology':
                t = WellMixedTopology(self.world, topid)
            else:
                # If the configured Topology is not one of the built-in types,
                # scan the plugins.
                if self.world.plugin_manager.plugin_exists(self.type):
                    oref = self.world.plugin_manager.get_plugin(self.type)
                    if oref == None:
                        print "Error: Couldn't find object ref for Topology type"
                    elif not issubclass(oref, Topology):
                        print "Error: Plugin %s is not an instance of Topology type" % (self.type)
                    else:
                        t = oref(self.world, topid)
                else:
                    print 'Error: Unknown Topology type'
	
        self.topologies.append(t)

    def update(self):
        """Update all topologies"""
        for top in self.topologies:
            top.update()

