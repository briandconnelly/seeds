# -*- coding: utf-8 -*-
"""
A Cell object represents a place in the environment where an organism could
reside.  If that Cell is occupied by an organism, the Cell object also defines
that organism.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


class Cell(object):
    """
    Interface for Cell objects

    Properties:
      experiment
        A reference to the Experiment in which the Cell exists
      population
        A reference to the Population in which the Cell exists
      id
        A unique ID representing that Cell.  This should be the same as the
        node id in the population topology graph.
      types
        List of strings describing the possible types the Cell could be
      type
        Number indicating which type the current Cell is.  This number
        is also an index into the 'types' parameter.
      coords
        Tuple of coordinates representing the location of the Cell in the
        environment

    Configuration:
        Configuration options for each custom Cell object should be stored in a
        configuration block bearing the name of that Cell type (e.g.,
        "[DemoCell]")

    """

    def __init__(self, experiment, population, id):
        """Initialize a Cell object

        Parameters:
        
        *experiment*
            A reference to the Experiment in which this Cell exists
        *population*
            A reference to the Population in which this Cell exists
        *id*
            A unique ID for this cell

        """

        self.experiment = experiment
        self.population = population
        self.id = id

    def __str__(self):
        """Produce a string to be used when a Cell object is printed"""
        return 'Cell %d Type %d' % (self.id, self.type)


    def get_neighbors(self):
        """Get a list of neighboring cells"""
        return [self.population.topology.graph.node[n]['cell'] for n in self.population.topology.get_neighbors(self.id)]

    def update(self):
        """Update the Cell according to its update rules"""
        pass

    def teardown(self):
        """Perform any necessary cleanup at the end of the experiment"""
        pass

