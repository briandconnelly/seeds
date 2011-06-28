# -*- coding: utf-8 -*-
"""
Handle a collection of Resource objects in a Cell
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.Resource import *
from seeds.SEEDSError import *

class ResourceManager(object):
    """
    Manage a Cell's Resources

    Each Cell object has a ResourceManager, which maintains a list of the
    Resources in that cell.

    """

    def __init__(self, experiment):
        """Initialize a ResourceManager object

        Parameters:
        
        *experiment*
            A reference to the Experiment

        """
        self.experiment = experiment
        self.resources = []

        try:
            self.init_resources()
        except ResourceTypePluginNotFoundError as err:
            raise ResourceTypePluginNotFoundError(err.resource)
        except TopologyPluginNotFoundError as err:
            raise TopologyPluginNotFoundError(err.topology)

    def init_resources(self):
        """Initialize all resources that will be available in this Experiment"""
        resourcestring = self.experiment.config.get("Experiment", "resources",
                                                    default="")
        if not resourcestring:
            return

        reslist = [res.strip() for res in resourcestring.split(',')]
        for res in reslist:
            sec = "Resource:%s" % (res)
            if not self.experiment.config.has_section(sec):
                raise ConfigurationError("No configuration for resource '%s'" % (res))

            r = Resource(experiment=self.experiment, name=res)
            self.resources.append(r)

    def get_level(self, name):
        """Get the level of a given resource

        Parameters:

        *name*
            The name of the Resource in question

        """
        for res in self.resources:
            if res.name == name:
                return res.get_level

    def get_resource(self, name):
        """Get the object associated with a given resource.  If the Resource
        does not exist, a ResourceNotDefinedError is raised.

        Parameters:

        *name*
            The name of the Resource in question

        """
        for res in self.resources:
            if res.name == name:
                return res

        raise ResourceNotDefinedError(name)

    def update(self):
        """Update all of the managed Resource objects"""
        [res.update() for res in self.resources]

    def teardown(self):
        """Clean up after all actions at the end of an experiment"""
        [res.teardown() for res in self.resources]

