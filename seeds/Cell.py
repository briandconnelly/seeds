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
        Number indicating which type the current Cell is.  This number is also
        an index into the 'types' parameter.
    max_types
        Maximum number of different types possible with this Cell
    type_colors
        A list of colors (matplotlib color strings or hex colors) to be used to
        represent the different cell types by scripts that plot or visualize
        the population.  A default list is defined that allows for coloring of
        up to 8 types.
    name
        The name of the Cell type
    label
        A unique label identifying this Cell's configuration

    Configuration:
        Configuration options for each custom Cell object should be stored in a
        configuration block bearing the name of that Cell type (e.g.,
        "[DemoCell]")

    """

    def __init__(self, experiment, population, id, name=None, label=None):
        """Initialize a Cell object

        Parameters:
        
        *experiment*
            A reference to the Experiment in which this Cell exists
        *population*
            A reference to the Population in which this Cell exists
        *id*
            A unique ID for this cell
        *name*
            The name of the Cell type
        *label*
            A unique label for the configuration of this cell

        """

        self.experiment = experiment
        self.population = population
        self.id = id
        self.name = name
        self.label = label
        self.type = None
        self.max_types = 0
        self.type_colors = ['r','g','b','y','c', 'm', 'k']

        if self.label:
            self.config_section = "%s:%s" % (self.name, self.label)
        else:
            self.config_section = "%s" % (self.name)

    def __str__(self):
        """Produce a string to be used when a Cell object is printed"""
        return 'Cell %d Type %d' % (self.id, self.type)

    def add_neighbor(self, neighbor):
        """Make the given cell a neighbor"""
        self.population.topology.add_edge(self.id, neighbor.id)

    def remove_neighbor(self, neighbor):
        """Disconnect the Cell from the given Cell, making them no longer
        neighbors
        """
        self.population.topology.remove_edge(self.id, neighbor.id)

    def get_neighbors(self):
        """Get a list of neighboring cells"""
        return [self.population.topology.graph.node[n]['cell'] for n in self.population.topology.get_neighbors(self.id)]

    def update(self):
        """Update the Cell according to its update rules"""
        pass

    def teardown(self):
        """Perform any necessary cleanup at the end of the experiment"""
        pass

    def coords(self):
        """Get the coordinates of the Cell in space"""
        return self.population.topology.graph.node[self.id]['coords']

    def get_neighbor_distance(self, neighbor):
        """Get the Cartesian distance to the given neighbor Cell"""
        return self.population.cell_distance(self, neighbor)

    def get_neighbor_distances(self):
        """Get an array of distances to all neighbors"""
        return [self.get_neighbor_distance(n) for n in self.get_neighbors()]
