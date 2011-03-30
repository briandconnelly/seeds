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
__version__ = "1.0.1"
__credits__ = "Brian Connelly, Luis Zaman, Ben Kerr"

from seeds.cell.Cell import *
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

    EMPTY = 0
    SENSITIVE = 1
    RESISTANT = 2
    PRODUCER = 3

    def __init__(self, world, topology, node, id, type=-1):
        """Initialize a Kerr07Cell object

        The type for the cell is selected at random.

        Parameters:

        *world*
            A reference to the World
        *topology*
            A reference to the topology in which the Cell will reside
        *node*
            A reference to the node on which the Cell exists
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

        self.ds = self.world.config.getfloat('Kerr07Cell', 'death_sensitive')
        self.dr = self.world.config.getfloat('Kerr07Cell', 'death_resistant')
        self.dp = self.world.config.getfloat('Kerr07Cell', 'death_producer')
        self.tp = self.world.config.getfloat('Kerr07Cell', 'toxicity')

    def __str__(self):
        """Produce a string to be used when the object is printed"""
        return 'Kerr07 Cell %d Type %d (%s)' % (self.id, self.type, self.types[self.type])

    def type(self):
        """Return the name of the type of this cell"""
        return self.types[self.type]

    def update(self, neighbors):
        """Update the cell based on its neighbors

        Empty cells will be replaced by a randomly-chosen neighbor cell. In
        this process, that neighbor cell effectively "reproduces" into the
        Empty cell.

        Sensitive cells may die due to their death rate or toxin produced by
        neighbors

        Resistant and Producer cells may die due to their death rate

        Parameters:

        *neighbors*
            A list of neighboring cells

        """

        typecount = {0: 0, 1: 0, 2: 0, 3: 0}

        if self.type == self.EMPTY:
            parent = random.choice(neighbors)
            self.type = parent.type
            self.topology.update_type_count(self.EMPTY, self.type)            

        elif self.type == self.SENSITIVE:
            for n in neighbors:
                typecount[n.type] += 1
        
            fs = float(typecount[self.SENSITIVE])/len(neighbors)
            fr = float(typecount[self.RESISTANT])/len(neighbors)
            fp = float(typecount[self.PRODUCER])/len(neighbors)
           
            if random.random() < (self.ds + self.tp * fp):
                self.type = self.EMPTY
                self.topology.update_type_count(self.SENSITIVE, self.EMPTY)            
                
        elif self.type == self.RESISTANT:
            if random.random() < self.dr:
                self.type = self.EMPTY
                self.topology.update_type_count(self.RESISTANT, self.EMPTY)            

        elif self.type == self.PRODUCER:
            if random.random() < self.dp:
                self.type = self.EMPTY
                self.topology.update_type_count(self.PRODUCER, self.EMPTY)            

        else:
            print 'Error: Invalid cell type %d for cell %d' % (self.type, self.id)

