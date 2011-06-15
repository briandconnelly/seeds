# -*- coding: utf-8 -*-
"""
Handle a collection of Resource objects in a Cell
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import re

from seeds.Resource import *
from seeds.ResourceGraph import *
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
        except ResourcePluginNotFoundError as err:
            # TODO: pass this error up somehow to stop the run
            print "Error:", err

    def init_resources(self):
        """Initialize all resources that will be available in this Experiment"""
        for res in self.experiment.config.get_resource_sections():
            match = re.match("Resource:(?P<resname>[a-zA-Z_0-9]+)", res)
            if match != None:
                name = match.group("resname")
                type = self.experiment.config.get(res, "type", default="NormalResource")
                available = self.experiment.config.getboolean(res, "available", default="True")

                try:
                    oref = self.experiment.plugin_manager.get_plugin(type, type=Resource)
                    r = oref(experiment=self.experiment, name=name, available=available)
                    self.resources.append(r)
                except PluginNotFoundError as err:
                    raise ResourcePluginNotFoundError(type)

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

