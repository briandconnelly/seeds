# -*- coding: utf-8 -*-
""" NormalResource ResourceCell represents resources that have some initial
level, which increases and decreases through inflow and decay, respectively.
Additionally, resources can flow between neighboring nodes through outflow.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.ResourceCell import *
from seeds.SEEDSError import *


class NormalResource(ResourceCell):
    """Environmental Resource class

    Properties:

    id
        A unique ID for this node in the resource graph
    experiment
        A reference to the Experiment being performed
    resource
        A reference to the Resource of which this object is a part
    level
        The current level of the resource
    config_section
        The name of the section where parameters for this object are defined
    inflow
        Amount of resource (in units) that flows into the environment per epoch
        (default: 0.0)
    decay
        Fraction of the resource that is removed from the environment per epoch
        (default: 0.0)
    outflow
        Fraction of resource difference (in percent) that flows into
        neighboring resource cells per epoch.  When a node is updated, the
        levels of its neighbors are checked.  The node then distributes some of
        its resource to these neighboring nodes, with the neighbor with the
        lowest level having first priority.  The difference between the levels
        of the two nodes is computed.  This is the maximum amount of resource
        that can flow to the neighboring cell.  Outflow is the percentage of
        this difference that is transferred.  At 0, no resource is transferred,
        while at 1, the entire difference (or as much as the node with higher
            resource has) between the two is transferred.  This would result in
            the neighboring node having a greater level than the focal node.
            This value can be seen to loosely represent viscosity. (default:
            0.5)
    initial
        The amount of resource (in units) present in the environment at the
        beginning (default: 0.0)

    NormalResource Resources can be defined in config files using a
    [Resource:<uniquename>] section and using the NormalResource type.  For
    example:

        [Resource:glucose]
        type = NormalResource
        topology = CartesianTopology
        initial = 0
        inflow = 0.24
        outflow = 0.1
        decay = 0.1

    The effects of outflow will depend on the topology, specifically the number
    of neighboring resource cells.

    """

    def __init__(self, experiment, resource, config_section, id):
        """ Initialize a NormalResource object

        Parameters:

        *experiment*
            A pointer to the Experiment
        *resource*
            A pointer to the Resource of which this is a part
        *config_section*
            The name under which the configuration parameters are specified for
            this Resource
        *id*
            A unique ID for this node in the resource graph

        """
        super(NormalResource, self).__init__(experiment=experiment,
                                             resource=resource,
                                             config_section=config_section,
                                             id=id)

        self.inflow = self.experiment.config.getfloat(self.config_section, "inflow", default=0.0)
        self.outflow = self.experiment.config.getfloat(self.config_section, "outflow", default=0.5)
        self.decay = self.experiment.config.getfloat(self.config_section, "decay", default=0.0)
        self.initial = self.experiment.config.getfloat(self.config_section, "initial", default=0.0)

        self.level = self.initial * 1.0

        if self.inflow < 0:
            raise ConfigurationError("NormalResource: inflow for '%s' can not be negative" % (self.resource.name))
        elif self.outflow < 0:
            raise ConfigurationError("NormalResource: outflow for '%s' can not be negative" % (self.resource.name))
        elif self.outflow > 1:
            raise ConfigurationError("NormalResource: outflow for '%s' can not be greater than 1" % (self.resource.name))
        elif self.decay < 0:
            raise ConfigurationError("NormalResource: decay for '%s' can not be negative" % (self.resource.name))
        elif self.decay > 1:
            raise ConfigurationError("NormalResource: decay for '%s' can not be greater than 1" % (self.resource.name))

    def __str__(self):
        """Produce a string to be used when a NormalResource object is printed"""
        return "NormalResource [Name: %s][Level: %f][Inflow: %f][Outflow: %f][Decay: %f]" % (self.name, self.level, self.inflow, self.outflow, self.decay)

    def set_inflow(self, value):
        """Set the inflow amount of the resource

        Parameters:

        *value*
            The new inflow amount of the resoruce

        """
        self.inflow = value

    def set_outflow(self, value):
        """Set the outflow rate of the resource

        Parameters:

        *value*
            The new outflow rate of the resoruce

        """
        self.outflow = value

    def set_decay(self, value):
        """Set the decay rate of the resource

        Parameters:

        *value*
            The new decay rate of the resoruce

        """
        self.decay = value

    def set_initial(self, value):
        """Set the initial level of the resource

        Parameters:

        *value*
            The new initial level of the resoruce

        """
        self.initial = value

    def update(self):
        """Update the level of the resource.  Even if the resource is
        unavailable, the resource level will be updated.
        
        """
        neighbors = self.get_neighbors()

        # Adjust the level based on inflow and decay
        newlevel = (self.level * (1 - self.decay)) + self.inflow
        self.level = max(0, newlevel)

        # Find the neighbors with lower levels
        low_neighbors = []
        for n in neighbors:
            if n.level < self.level:
                low_neighbors.append((n.level,n))
        low_neighbors.sort()

        # Go through the neighboring nodes and transfer some resource to those
        # nodes as long as level is still above them.  Priority is given to
        # nodes with the lowest level.
        for (lvl,n) in low_neighbors:
            if self.level > n.level:
                xfer = min(self.level, self.level - n.level) * self.outflow
                n.level += xfer
                self.level -= xfer

        self.level = max(0, newlevel)
        self.experiment.data['resources'][self.resource.name]['levels'][self.id] = self.level

