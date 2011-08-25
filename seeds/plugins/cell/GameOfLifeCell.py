# -*- coding: utf-8 -*-
""" Cell type modeling the Conway's classic Game of Life cellular automaton.
Each cell is either "Alive" or "Dead", and when a cell is updated, it follows
the following rule:

- Live cells with less than 2 neighbors die (under-population)
- Live cells with 2 or 3 neighbors live
- Live cells with more than 3 neighbors die (overcrowding)
- Dead cells with 3 neighbors becomes alive (birth)

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import random

from seeds.Cell import *
from seeds.SEEDSError import *


class GameOfLifeCell(Cell):
    """
    This is a simple Cell type modeling Conway's Game of Life.

    This Cell type has 2 states:
        ALIVE: Cells that are alive
        DEAD: Cells that are dead

    """

    types = ['Alive', 'Dead']
    type_colors = ['k','w']
    max_types = 2

    ALIVE = 0
    DEAD = 1

    def __init__(self, experiment, population, node, type=None, name="GameOfLifeCell", label=None):
        """Initialize a GameOfLifeCell object

        The type for the cell is selected at random.

        Parameters:

        *experiment*
            A reference to the Experiment
        *population*
            A reference to the Population in which this Cell exists
        *node*
            The ID of the node on which this Cell resides
        *type*
            The type of cell to initialize (If none provided, type randomly assigned)
        *name*
            The name of this Cell type
        *label*
            A unique label for configuring this Cell type

        """

        super(GameOfLifeCell, self).__init__(experiment, population, node=node, type=type, name=name, label=label)
        self.population.increment_type_count(self.type)

    def __str__(self):
        """Produce a string to be used when the object is printed"""
        return 'GameOfLifeCell %d Type %d (%s)' % (self.id, self.type, self.types[self.type])

    def type(self):
        """Return the name of the type of this cell"""
        return self.types[self.type]

    def update(self):
        """Update the cell based on the following rules:

        - Live cells with less than 2 neighbors die (under-population)
        - Live cells with 2 or 3 neighbors live
        - Live cells with more than 3 neighbors die (overcrowding)
        - Dead cells with 3 neighbors becomes alive (birth)

        """

        if len(self.neighbors) < 1:
            print("Warning: Can not update GameOfLifeCell with 0 neighbors")
            return

        num_live_neighbors = 0
        num_dead_neighbors = 0

        for n in self.neighbors:
            if n.type == self.ALIVE: num_live_neighbors += 1
            elif n.type == self.DEAD: num_dead_neighbors += 1

        if self.type == self.ALIVE and num_live_neighbors < 2:
            self.type = self.DEAD
            self.population.update_type_count(self.ALIVE, self.DEAD)            
        elif self.type == self.ALIVE and num_live_neighbors > 3:
            self.type = self.DEAD
            self.population.update_type_count(self.ALIVE, self.DEAD)            
        elif self.type == self.DEAD and num_live_neighbors == 3:
            self.type = self.ALIVE
            self.population.update_type_count(self.DEAD, self.ALIVE)            
