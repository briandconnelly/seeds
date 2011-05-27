# -*- coding: utf-8 -*-
""" This is a template to aid in the understanding and creation of Cell types.
Places where the user should enter or change code are indicated with TODO.  For
more information, see the "Creating Cells" on the SEEDS Wiki.  For a simple example,
see RPSCell.py in seeds/plugins/cell.

TODO: Detailed description of the Cell type
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.Cell import *
import random

class TODO-CellName(Cell):
    """
    TODO: description of this class including what it represents, which
    parameters it has, and how it can be configured.
    """

    # TODO: fill in the types variable, which is a list of the names of the
    # types a cell can be.
    types = ['TODO type1', 'TODO type2']

    def __init__(self, experiment, topology, node, id, type=-1):
        """TODO: additional information for this Cell type's constructor

        Parameters:

        *experiment*
            A reference to the Experiment
        *topology*
            A reference to the topology in which the Cell will reside
        *node*
            A reference to the node on which the Cell resides
        *id*
            A unique ID for the cell
        *type*
            The type of cell to initialize (-1 for random)

        """

        super(TODO-CellName, self).__init__(experiment,topology,node,id)

        if type == -1:
            self.type = random.randint(0,len(self.types)-1)
        else:
            self.type = type
        
        self.topology.increment_type_count(self.type)

    def __str__(self):
        """Produce a string to be used when the object is printed"""
        # TODO: although not completely necessary, it's nice to have a unique
        # description for your Cell type
        return 'RPSCell %d Type %d (%s)' % (self.id, self.type, self.types[self.type])

    def type(self):
        """Return the name of the type of this cell"""
        return self.types[self.type]

    def update(self, neighbors):
        """TODO: comments describing the Cell update process

        Parameters:

        *neighbors*
            A list of neighboring cells

        """

        # TODO: update the current Cell.  This can be based on all of its
        # neighbors, a randomly-selected neighbor, or some other factor.

        # TODO: If there are more than one type for this cell, update the type
        # counts for the cells.  This speeds up actions that produce output
        # based on these counts by preventing all cells to be scanned whenever
        # they are run.  If there is only one type, this line can simply be
        # removed.

        self.topology.update_type_count(self.OLD_TYPE_NUMBER, self.NEW_TYPE_NUMBER)

