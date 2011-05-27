# -*- coding: utf-8 -*-
""" A Resource object represents the amount of a particular resource at a given
location in space.  Resources have a level that can be checked, consumed, or
added to.  Different Resource objects may have different objects such as inflow
and may interact with neighboring Resource objects (e.g., for diffusion).

This class provides the base properties and functionality for all Resources
used in SEEDS.  Specific implementations can be seen in plugins/resource.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


class Resource(object):
    """Interface for Resources

    Properties:

    name
        Unique name of the resource
    available
        Whether or not the resource is currently available (default: True)
    level
        Current level of the resource

    Resources are defined in config files using a [Resource:<uniquename>]
    section.  For example:

    [Resource:glucose}
    type = NormalResource
    initial = 10.0
    inflow = 1
    outflow = 0.1
    decay = 0.1

    For more information about the properties of this resource, see the
    documentation for NormalResource.

    """

    def __init__(self, experiment, name=None, available=True):
        """ Initialize a Resource object

        Parameters:

        *experiment*
            A pointer to the Experiment
        *name*
            A name for the resource
        *available*
            Whether or not the resource is currently available (default: True).
            When a resource is unavailable, get_level will return a level of
            0.0.

        """

        self.experiment = experiment

        if name != None:
            self.name = name
        else:
            print "Error: Must supply Resource name"

        self.config_section = "Resource:%s" % (name)
        self.available = available
        self.level = 0.0

    def __str__(self):
        """Produce a string to be used when a Resource object is printed"""
        return "Resource [Name: %s][Level: %f]" % (self.name, self.level)

    def set_level(self, value):
        """Set the level of the resource

        Parameters:

        *value*
            The new level of the resoruce

        """
        self.level = value

    def get_level(self):
        """Return the current level of the resource.  If it is not available,
        0.0 will be returned.

        """

        if self.available:
            return self.level
        else:
            return 0.0

    def update(self):
        """Update the level of the resource.  Even if the resource is
        unavailable, the resource level will be updated.
        
        """
        pass

    def teardown(self):
        """Perform any necessary cleanup at the end of the experiment"""
        pass

