# -*- coding: utf-8 -*-
""" A population stores information related to the organisms that exist in an
experiment, including the graph that defines their interactions and a
dictionary to store any additional information about the population as a whole.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.Experiment import *
from seeds.Topology import *


class Population(object):
    """Manage populations of organisms

    Properties:

    data
        A dict that can be used to store additional data about a population.
        For example, see the 'type_count' value, which is used to store the
        counts of different cell types (for cells that have different types)
        across the population.  This is faster than scanning the population
        whenever this information is needed.
    experiment
        A reference to the Experiment in which this Population exists
    topology
        A graph representing the organisms (nodes) and the potential
        interactions between them (edges)

    """

    def __init__(self, experiment):
        self.experiment = experiment
        self.data = {}
        self.data['type_count'] = []
        self.topology = self.experiment._population_topology_class(self.experiment, self)

    def update(self):
        """Update the Population: update the topology"""
        self.topology.update()

    def teardown(self):
        """Perform teardown at the end of an experiment"""
        self.topology.teardown()

    def increment_type_count(self, type):
        """Increment the cell type count for the given type

        Parameters:

        *type*
            The cell type whose count to increment

        """

        if len(self.data['type_count']) <= type:
            self.data['type_count'].extend([0] * (1 + type-len(self.data['type_count'])))
        self.data['type_count'][type] += 1

    def decrement_type_count(self, type):
        """Decrement the cell type count for the given type

        Parameters:

        *type*
            cell type whose count to decrement

        """

        self.data['type_count'][type] -= 1

    def update_type_count(self, fromtype, totype):

        """Update the cell type counts, subtracting from the 'from' type and
        adding to the 'to' type

        Parameters:

        *fromtype*
            type that a cell was prior to being updated
        totype*
            type that a cell is after being updated

        """

        self.decrement_type_count(fromtype)
        self.increment_type_count(totype)

