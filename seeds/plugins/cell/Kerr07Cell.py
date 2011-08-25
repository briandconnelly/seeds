# -*- coding: utf-8 -*-
""" Cell type that represents bacteriocin-producing bacteria.  In this system,
cells can be either toxin producers, toxin resistant, or toxin sensitive.
Toxin producers produce a toxin that kills nearby sensitive cells.  This toxin
does not effect resistant or producer cells.

The costs of toxin resistance and production each manifest themselves as
increases in mortality.  Therefore, producers have the highest death rate,
followed by resistant cells, and finally sensitive cells.

This is a non-transitive system that can be compared with the
rock-paper-scissors (RPS) game, where each strategy beats one but is beaten by
another.  If any one strategy is lost, another strategy will also be lost, as
the non-transitivity is broken (if no one can play 'rock', 'scissors' will
always win the game).

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly, Luis Zaman, Ben Kerr"

from seeds.Cell import *
import random

class Kerr07Cell(Cell):
    """
    This is a Cell type inspired by the model presented in:

        B. Kerr, Bacteriocins: ecology and evolution. Springer, 2007

    and used in:

        B.D. Connelly, L. Zaman, C. Ofria, and P.K. McKinley,
        "Social structure and the maintenance of biodiversity," in
        Proceedings of the 12th International Conference on the Synthesis
        and Simulation of Living Systems (ALIFE), pp. 461-468, 2010.

    This Cell type has 4 states:
        EMPTY: no organism is in the cell
        SENSITIVE: cells sensitive to being killed by bacteriocin
        RESISTANT: cells insensitive to bacteriocin, but that do not
          produce it themselves.
        PRODUCER: cells that produce bacteriocin and are insensitive
          to it.

    The sensitivity of a SENSITIVE cell to bacteriocin depends on the
    number of PRODUCER cells in its neighborhood.


    Configuration: All configuration options should be specified in a
    Kerr07Cell block.

        death_sensitive: death rate of SENSITIVE cells (float, [0,1])
        death_resistant: death rate of RESISTANT cells (float, [0,1])
        death_producer: death rate of PRODUCER cells (float, [0,1])
        toxicity: The toxicity of PRODUCER cells (float, [0,1])

    Example:
        [Kerr07Cell]
        death_sensitive = 0.250
        death_resistant = 0.312
        death_producer = 0.333
        toxicity = 0.650

    """

    types = ['Empty', 'Sensitive', 'Resistant', 'Producer']
    max_types = 4
    type_colors = ['#777777','b','g','r']

    EMPTY = 0
    SENSITIVE = 1
    RESISTANT = 2
    PRODUCER = 3

    def __init__(self, experiment, population, node, type=None, name="Kerr07Cell", label=None):
        """Initialize a Kerr07Cell object

        The type for the cell is selected at random.

        Parameters:

        *experiment*
            A reference to the Experiment in which the Cell will reside
        *population*
            A reference to the Population in which this Cell resides
        *node*
            The ID of the node on which this Cell resides
        *type*
            The type of cell to initialize (randomly chosen if not provided)
        *name*
            The name of this Cell type
        *label*
            A unique label for configuring this Cell type

        """

        super(Kerr07Cell, self).__init__(experiment, population, node=node, type=type, name=name, label=label)
        self.population.increment_type_count(self.type)

        self.ds = self.experiment.config.getfloat(self.config_section, 'death_sensitive')
        self.dr = self.experiment.config.getfloat(self.config_section, 'death_resistant')
        self.dp = self.experiment.config.getfloat(self.config_section, 'death_producer')
        self.tp = self.experiment.config.getfloat(self.config_section, 'toxicity')

    def __str__(self):
        """Produce a string to be used when the object is printed"""
        return 'Kerr07 Cell %d Type %d (%s)' % (self.id, self.type, self.types[self.type])

    def type(self):
        """Return the name of the type of this cell"""
        return self.types[self.type]

    def update(self):
        """Update the cell based on its neighbors

        Empty cells will be replaced by a randomly-chosen neighbor cell. In
        this process, that neighbor cell effectively "reproduces" into the
        Empty cell.

        Sensitive cells may die due to their death rate or toxin produced by
        neighbors

        Resistant and Producer cells may die due to their death rate

        """

        typecount = {0: 0, 1: 0, 2: 0, 3: 0}

        if self.type == self.EMPTY:
            parent = random.choice(self.neighbors)
            self.type = parent.type
            self.population.update_type_count(self.EMPTY, self.type)            

        elif self.type == self.SENSITIVE:
            for n in self.neighbors:
                typecount[n.type] += 1

            num_neighbors = len(self.neighbors)
        
            fs = float(typecount[self.SENSITIVE])/num_neighbors
            fr = float(typecount[self.RESISTANT])/num_neighbors
            fp = float(typecount[self.PRODUCER])/num_neighbors
           
            if random.random() < (self.ds + self.tp * fp):
                self.type = self.EMPTY
                self.population.update_type_count(self.SENSITIVE, self.EMPTY)            
                
        elif self.type == self.RESISTANT:
            if random.random() < self.dr:
                self.type = self.EMPTY
                self.population.update_type_count(self.RESISTANT, self.EMPTY)            

        elif self.type == self.PRODUCER:
            if random.random() < self.dp:
                self.type = self.EMPTY
                self.population.update_type_count(self.PRODUCER, self.EMPTY)            

        else:
            print("Error: Invalid cell type %d for cell %d" % (self.type, self.id))
