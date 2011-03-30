# -*- coding: utf-8 -*-
"""
A Cell object represents a place in the world where an organism could reside.
If that Cell is occupied by an organism, the Cell object also defines that
organism.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.2"
__credits__ = "Brian Connelly"


class Cell(object):
    """
    Interface for Cell objects

    Properties:
      world
        A reference to the World in which the Cell exists
      topology
        A reference to the specific Topology in which the Cell exists
      node
        A reference to the node on which the Cell exists (for resource access)
      id
        A unique ID representing that Cell (at minimum, unique to its Topology)
      types
        List of strings describing the possible types the Cell could be
      type
        Number indicating which type the current Cell is.  This number
        is also an index into the 'types' parameter.
      coords
        Tuple of coordinates representing the location of the Cell in the
        Topology

    Configuration:
        Configuration options for each custom Cell object should be stored in a
        configuration block bearing the name of that Cell type (e.g.,
        "[DemoCell]")

    """

    def __init__(self, world, topology, node, id):
        """Initialize a Cell object

        Parameters:
        
        *world*
            A reference to the World
        *topology*
            A reference to the Topology in which this Cell exists
        *node*
            A reference to the graph node on which the Cell exists
        *id*
            A unique ID for this cell

        """

        self.world = world
        self.topology = topology
        self.node = node
        self.id = id

    def __str__(self):
        """Produce a string to be used when a Cell object is printed"""
        return 'Cell %d Type %d' % (self.id, self.type)


    def get_neighbors(self):
        """Get a list of neighboring cells"""

    def update(self, neighbors):
        """Update the Cell given a list of neighboring Cells
        
        Parameters:

        *neighbors*
            A list of Cell objects that are neighboring this cell in the topology

        """
        pass

