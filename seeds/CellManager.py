# -*- coding: utf-8 -*-
"""
Manage Cell objects and initialize the right type based on the
configuration

If the configured Cell is not part of the standard SEEDS ones, the plugin
manager will be used to see if it has been defined by the user.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.2"
__credits__ = "Brian Connelly, Luis Zaman"

import seeds.cell
from seeds.cell import *

from seeds.PluginManager import *


class CellManager(object):
    """ The purpose of the cell manager is to initialize Cell objects of the
    correct type, as specified by the "cell" parameter in the [Experiment]
    block in the configuration.

    """

    def __init__(self, world, topology):
        """Initialize a CellManager object

        Parameters:

        *world*
            A reference to the World object
        *topology*
            A reference to the Topology object in which the Cell will reside

        """

        self.world = world
        self.topology = topology
        self.type = self.world.config.get('Experiment', 'cell')

    def newcell(self, node, id):
        """Create a new Cell object"""
        if self.type == 'Cell':
            c = Cell(self.world, self.topology, node, id)
        elif self.type == 'Kerr07Cell':
            c = Kerr07Cell(self.world, self.topology, node, id)
        elif self.type == 'RPSCell':
            c = RPSCell(self.world, self.topology, node, id)
        else:
            # If the configured Cell is not one of the built-in types,
            # scan the plugins.
            if self.world.plugin_manager.plugin_exists(self.type):
                oref = self.world.plugin_manager.get_plugin(self.type)
                if oref == None:
                    print "Error: Couldn't find object ref for Cell type"
                elif not issubclass(oref, Cell):
                    print "Error: Plugin %s is not an instance of Cell type" % (self.type)
                else:
                    c = oref(self.world, self.topology, node, id)
            else:
                print 'Error: Unknown Cell type'

        return c

