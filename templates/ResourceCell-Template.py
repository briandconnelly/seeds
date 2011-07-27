# -*- coding: utf-8 -*-

""" This template outlines the necessary components for implementing a new
ResourceCell in SEEDS.  Generally, this involves implementing a constructor
(__init__) and an update method.  In SEEDS, Resources are modeled as graphs of
ResourceCell nodes, which define the Resource at a specific location in the
world.

Areas marked with 'TODO' should be replaced with code specific to the
ResourceCell being implemented.

The name of the ResourceCell type should be the name of the class.  The name of
the file should also match this.

Methods and parameters common to all ResourceCell objects can be seen in the
ResourceCell.py file in the main SEEDS codebase.

Once completed, new ResourceCell type files can be placed in a plugins
directory and used by specifying the name of the file/class with the "type"
parameter in the appropriate [Resource] section of the configuration file.

"""

__author__ = "TODO"
__credits__ = "TODO"

from seeds.Action import *
from seeds.ResourceCell import *
from seeds.SEEDSError import *


class TODO-ResourceCellName(ResourceCell):
    """ TODO: Documentation for this ResourceCell type including its
    motivations, how it is configured, and how it works.

    """

    # TODO: constructor for ResourceCell objects.
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

        # TODO: get configuration values.  Here, "inflow" is used for example purposes.
        self.inflow = self.experiment.config.getfloat(self.config_section, "inflow", default=0.0)

        # TODO: validate any configuration values
        if self.inflow < 0:
            raise ConfigurationError("NormalResource: inflow for '%s' can not be negative" % (self.resource.name))

        # TODO: initialize the ResourceCell
        self.level = 0.0

    # TODO: the __str__ method returns a string to be used when an object is
    # printed.  This can be a useful place to return information that is
    # specific to the ResourceCell type
    def __str__(self):
        """Produce a string to be used when an object is printed"""
        return "TODO-ResourceCellName [Name: %s][Level: %f]" % (self.name, self.level)


    # TODO: the update method updates the level of the resouce according to the
    # rules for this ResourceCell.

    def update(self):
        """Update the level of the resource.  Even if the resource is
        unavailable, the resource level will be updated.
        
        """

        # NOTE: If the state depends on neighbors, the list of neighbor
        # ResourceCells can be retrieved.
        neighbors = self.get_neighbors()

        # TODO: calculate the new level
        self.level = TODO

        # NOE: The levels of all ResourceCells are kept in a list.  This
        # enables information about the distribution of resources to be
        # retrieved without traversing the graph.  Here, we update the level
        # associated with this cell.
        self.experiment.data['resources'][self.resource.name]['levels'][self.id] = self.level


# TODO: typically, any Actions associated with this ResourceCell type are also
# defined in this file.  Refer to the Action template for more information.
