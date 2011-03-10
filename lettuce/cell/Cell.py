"""
A Cell object represents a place in the world where an organism could reside.
If that Cell is occupied by an organism, the Cell object also defines that
organism.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "0.9.0"
__credits__ = "Brian Connelly"

from lettuce.Resource import *
from lettuce.ResourceManager import *

import re

class Cell(object):
    """
    Interface for Cell objects

    Properties:
      world
        A reference to the World in which the Cell exists
      topology
        A reference to the specific Topology in which the Cell exists
      id
        A unique ID representing that Cell (at minimum, unique to its Topology)
      types
        List of strings describing the possible types the Cell could be
      type
        Number indicating which type the current Cell is.  This number
        is also an index into the 'types' parameter.
      resource_manager
        A resource manager to handle resource levels in each Cell
      coords
        Tuple of coordinates representing the location of the Cell in the
        Topology

    Configuration:
        Configuration options for each custom Cell object should be stored in a
        configuration block bearing the name of that Cell type (e.g.,
        "[DemoCell]")

    """

    def __init__(self, world, topology, id):
        """Initialize a Cell object

        Parameters:
        
        *world*
            A reference to the World
        *topology*
            A reference to the Topology in which this Cell exists
        *id*
            A unique ID for this cell

        """

        self.world = world
        self.topology = topology
        self.resource_manager = ResourceManager(world, topology)
        self.init_resources()

    def __str__(self):
        """Produce a string to be used when a Cell object is printed"""
        return 'Cell %d Type %d' % (self.id, self.type)

    def init_resources(self):
        """Initialize all resources that will be associated with this Cell"""
        for res in self.world.config.get_resource_sections():
            match = re.match("Resource:(?P<resname>[a-zA-Z_]+)", res)
            if match != None:
                name = match.group("resname")

            initial = self.world.config.getfloat(res, 'initial')
            inflow = self.world.config.getfloat(res, 'inflow')
            outflow = self.world.config.getfloat(res, 'outflow')

            r = Resource(name=name, initial=initial, inflow=inflow, outflow=outflow)
            self.resource_manager.add_resource(r)

    def update(self, neighbors):
        """Update the Cell given a list of neighboring Cells

        Parameters:

        *neighbors*
            A list of Cell objects that are neighboring this cell in the topology

        """

        pass

