"""
Manage Cell objects and initialize the right type based on the
configuration

If the configured Cell is not part of the standard Lettuce ones, the plugin
manager will be used to see if it has been defined by the user.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "0.9.0"
__credits__ = "Brian Connelly, Luis Zaman"

import lettuce.cell
from lettuce.cell import *

from lettuce.PluginManager import *


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

    def newcell(self, id):
        """Create a new Cell object"""
        if self.type == 'Cell':
            c = Cell(self.world, self.topology, id)
        elif self.type == 'Kerr07':
            c = Kerr07Cell(self.world, self.topology, id)
        elif self.type == 'GECCO2011':
            c = GECCO2011Cell(self.world, self.topology, id)
        elif self.type == 'RPSCell':
            c = RPSCell(self.world, self.topology, id)
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
                    c = oref(self.world, self.topology, id)
            else:
                print 'Error: Unknown Cell type'

        return c

