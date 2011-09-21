# -*- coding: utf-8 -*-

""" This template outlines the necessary components for implementing a new Cell
in SEEDS.  Generally, this involves implementing a constructor (__init__) and
an update method.

Areas marked with 'TODO' should be replaced with code specific to the Cell
being implemented.

The name of the Cell type should be the name of the class.  The name of the
file should also match this.

Methods and parameters common to all Cell objects can be seen in the Cell.py
file in the main SEEDS codebase.

Once completed, new Cell type files can be placed in a plugins directory and
used by specifying the name of the file/class with the "cell" parameter in the
[Population] section of the configuration file.

"""

__author__ = "TODO"
__credits__ = "TODO"

import random

from seeds.Cell import *
from seeds.SEEDSError import *


class TODO-CellTypeName(Cell):

    """ TODO - some documentation about this Cell, the motivation behind it,
    and the configuration parameters it accepts.

    """

    # TODO: the "types" list specifies the different types of Cell that this
    # model supports.

    # TODO: the "max_types" property describes the maximum number of types
    # possible with this cell type.  Generally, this is equal to the length of
    # the "types" list, however it is possible to have more complex Cell types.
    # For example, one could assign a type for all unique genomes in a genetic
    # algorithm (GA) model.

    # TODO: the "type" colors list specifies the colors that should be used to
    # represent each Cell type in actions that produce images or movies.  The
    # length of this list should be equal to the length of the "types" list.

    types = ['Rock', 'Paper', 'Scissors']
    max_types = 3
    type_colors = ['r','g','b']

    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    # TODO: the __init__ method (or "constructor") is called when a new Cell
    # object is created.  Generally, a Cell type will want to be assigned
    # during this step as well as any other properties associated with this
    # Cell.  This is often the stage where configuration values are read.

    def __init__(self, experiment, population, node, type=None,
                 name="TODO-CellTypeName", label=None):
        """
        TODO: documentation
        """

        # Call the Cell constructor, assigning properties common to all cells.
        # The type will be assigned by Cell's constructor and stored in self.type

        super(TODO-CellTypeName, self).__init__(experiment, population,
                                                node=node, type=type,
                                                name=name, label=label)

        # Keep track of how many organisms there are of this type.  You will
        # probably want to keep this code.
        self.population.increment_type_count(self.type)

        # TODO: read any configuration values


    # TODO: the __str__ method returns a string to be used when an object is
    # printed.  This can be a useful place to return information that is
    # specific to the Cell type
    def __str__(self):
        """Produce a string to be used when the object is printed"""
        return 'TODO-CellTypeName %d Type %d (%s)' % (self.id, self.type, self.types[self.type])

    def type(self):
        """Return the name of the type of this cell"""
        return self.types[self.type]


    # TODO: the update method updates an organism's state.  As such, it is the
    # most important part of a Cell object.  When a Cell is updated, it may
    # update its state based on environmental conditions, the composition of
    # its neighborhood, or through stochastic processes.  This dependes
    # completely on the type of system being modeled.

    def update(self):
        """
        TODO: documentation about how a Cell is updated
        """

        # If state is updated based on the composition of the neighborhood,
        # this code updates the list of neighboring Cell objects.
        self.neighbors = self.get_neighbors()

        # If a Cell's state depends on the level of some resource, at that
        # point in space, the following sample code gets the nearest cell for
        # that resource and sets its value.
        res = self.experiment.get_resource("RESOURCE_NAME")
        res_node = res.topology.get_nearest_node(coords=self.coords(), n=1)[0]
        res_cell = res.topology.graph.node[res_node]['resource']
        print("Current Resource Level: %f" % (res_cell.level))

        res_cell.level = max(0, res_cell.level - 1) # Consume up to 1 unit of resource


        # If the type of the Cell changes, the update_type_count method should
        # be called, which specifies the old type and the new type.
        self.population.update_type_count(OLD_TYPE, NEW_TYPE)

