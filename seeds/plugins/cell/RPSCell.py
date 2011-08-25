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
__credits__ = "Brian Connelly"

import random

from seeds.Cell import *
from seeds.SEEDSError import *
from seeds.utils.sampling import roulette_select


class RPSCell(Cell):
    """
    This is a simple Cell type modeling the classic Rock-Paper-Scissors (RPS)
    game.

    This Cell type has 3 states:
        ROCK: Outcompetes SCISSORS cells
        PAPER: Outcompetes ROCK cells
        SCISSORS: Outcompetes PAPER cells

    Configuration: The following configuration parameters can be configured in
    the [RPSCell] section of the config.

    distance_dependent
        Whether or not a Cell is more likely to interact with nearby
        neighboring Cells.  In this case, the probability of interacting with a
        given neighbor is proportional to the distance to that neighbor.
        (Default: False)

    """

    types = ['Rock', 'Paper', 'Scissors']
    type_colors = ['r','g','b']
    max_types = 3

    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    def __init__(self, experiment, population, node, type=None, name="RPSCell", label=None):
        """Initialize a RPSCell object

        The type for the cell is selected at random.

        Parameters:

        *experiment*
            A reference to the Experiment
        *population*
            A reference to the Population in which this Cell exists
        *node*
            The ID of the node on which this Cell resides
        *type*
            The type of cell to initialize (assigned randomly if not provided)
        *name*
            The name of this Cell type
        *label*
            A unique label for configuring this Cell type

        """

        super(RPSCell, self).__init__(experiment, population, node=node, type=type, name=name, label=label)
        self.population.increment_type_count(self.type)

        self.distance_dependent = self.experiment.config.getboolean(section=self.config_section,
                                                                    name='distance_dependent',
                                                                    default=False)

    def __str__(self):
        """Produce a string to be used when the object is printed"""
        return 'RPSCell %d Type %d (%s)' % (self.id, self.type, self.types[self.type])

    def type(self):
        """Return the name of the type of this cell"""
        return self.types[self.type]

    def update(self):
        """Update the cell based on a competition with a randomly-selected
        neighbor

        Rock cells will be replaced by paper cells.  Paper cells will be
        replaced by Scissors cells.  Scissors cells will be replaced by Rock
        cells.

        If a Cell has no neighbors, the Cell can not be updated.  In this case,
        a warning is printed.

        """

        if len(self.neighbors) < 1:
            print("Warning: Can not update RPSCell with 0 neighbors")
            return

        if self.distance_dependent:
            # Select a competitor with probability proportional to the
            # closeness of that neighbor (roulette wheel)

            # Adding a very small number to the distances to prevent
            # divide-by-zero errors, which can occur in well-mixed topologies,
            # where a Cell can exist in its own neighbor list

            distances = self.get_neighbor_distances()
            inv_dist = [1.0/(d + pow(1.02,-10000)) for d in distances]
            competitor = roulette_select(items=self.neighbors, fitnesses=inv_dist, k=1)[0]
        else:
            # Pick a random neighbor to compete with.  If that neighbor wins, it
            # gets the current cell.
            competitor = random.choice(self.neighbors)

        if self.type == self.ROCK and competitor.type == self.PAPER:
            self.type = self.PAPER
            self.population.update_type_count(self.ROCK, self.type)            
            self.id = self.population.get_cell_id()
        elif self.type == self.PAPER and competitor.type == self.SCISSORS:
            self.type = self.SCISSORS
            self.population.update_type_count(self.PAPER, self.type)            
            self.id = self.population.get_cell_id()
        elif self.type == self.SCISSORS and competitor.type == self.ROCK:
            self.type = self.ROCK
            self.population.update_type_count(self.SCISSORS, self.type)            
            self.id = self.population.get_cell_id()
