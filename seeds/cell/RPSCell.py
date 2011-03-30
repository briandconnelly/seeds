# -*- coding: utf-8 -*-
""" Cell type representing the classic game Rock-Paper-Scissors (RPS).  In this
system, a cell can be either a rock, paper, or scissors.  Rock is defeated by
paper, paper is defeated by scissors, and scissors is defeated by rock.  This
is a non-transitive system, where each strategy beats one but is beaten by
another.  If any one strategy is lost, another strategy will also be lost, as
the non-transitivity is broken (e.g., if no one can play rock, scissors will
always win the game).

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.2"
__credits__ = "Brian Connelly"

from seeds.cell.Cell import *
import random

class RPSCell(Cell):
    """
    This is a simple Cell type modeling the classic Rock-Paper-Scissors (RPS)
    game.

    This Cell type has 3 states:
        ROCK: Outcompetes SCISSORS cells
        PAPER: Outcompetes ROCK cells
        SCISSORS: Outcompetes PAPER cells

    Configuration: There are no parameters configurable for this Cell type.

    """

    types = ['Rock', 'Paper', 'Scissors']

    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    def __init__(self, world, topology, node, id, type=-1):
        """Initialize a RPSCell object

        The type for the cell is selected at random.

        Parameters:

        *world*
            A reference to the World
        *topology*
            A reference to the topology in which the Cell will reside
        *node*
            A reference to the node on which the Cell resides
        *id*
            A unique ID for the cell
        *type*
            The type of cell to initialize (-1 for random)

        """

        Cell.__init__(self,world,topology,node,id)

        if type == -1:
            self.type = random.randint(0,len(self.types)-1)
        else:
            self.type = type
        
        self.topology.increment_type_count(self.type)

    def __str__(self):
        """Produce a string to be used when the object is printed"""
        return 'RPSCell %d Type %d (%s)' % (self.id, self.type, self.types[self.type])

    def type(self):
        """Return the name of the type of this cell"""
        return self.types[self.type]

    def update(self, neighbors):
        """Update the cell based on a competition with a randomly-selected
        neighbor

        Rock cells will be replaced by paper cells.  Paper cells will be
        replaced by Scissors cells.  Scissors cells will be replaced by Rock
        cells.

        Parameters:

        *neighbors*
            A list of neighboring cells

        """

        # Pick a random neighbor to compete with.  If that neighbor wins, it
        # gets the current cell.
        competitor = random.choice(neighbors)

        if self.type == self.ROCK and competitor.type == self.PAPER:
            self.type = self.PAPER
            self.topology.update_type_count(self.ROCK, self.type)            
        elif self.type == self.PAPER and competitor.type == self.SCISSORS:
            self.type = self.SCISSORS
            self.topology.update_type_count(self.PAPER, self.type)            
        elif self.type == self.SCISSORS and competitor.type == self.ROCK:
            self.type = self.ROCK
            self.topology.update_type_count(self.SCISSORS, self.type)            

