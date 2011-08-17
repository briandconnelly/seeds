# -*- coding: utf-8 -*-
"""
Manage plugins for the system

Plugins allow SEEDS to be extended to suit the needs of users without adding
to the base code and adding additional dependencies.  Examples include
additional Cells, Topologies, or Actions.  Plugins may be stored in multiple
directories.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


import imp
import os
import sys

from seeds.Action import *
from seeds.Cell import *
from seeds.ResourceCell import *
from seeds.SEEDSError import *
from seeds.Topology import *

class PluginManager(object):
    """ The PluginManager object keeps track of plugins in the specified plugin
    directories and allows users to query these plugins and receive references
    to the resulting objects.

    Properties:

    experiment
        A reference to the Experiment
    plugin_dirs
        A list of directories that may contain plugins
    plugins
        A module object containing attributes for each loaded plugin
        

    Configuration:
    
    The directories in which plugins can be searched for are specified by the
    plugin_dirs parameter in the [Experiment] block as a comma-separated list.

    Example:

    [Experiment]
    plugin_dirs = plugins,/opt/seedsplugins,../old_plugins

    """

    def __init__(self, experiment):
        """Initialize a PluginManager object

        Parameters:

        *experiment*
            A reference to the Experiment
        """

        self.experiment = experiment
        self.plugin_dirs = []
        self.plugins = None

        plugindirs = self.experiment.config.get(section=self.experiment.config_section, name='plugin_dirs')
        if plugindirs:
            for d in plugindirs.split(','):
                if os.path.exists(d):
                    self.append_dir(d)

    def load_plugins(self):
        """Scan the plugin directories and load the plugins"""

        self.plugins = None

        for plugindir in self.plugin_dirs:
            if os.path.exists(plugindir) and os.path.isdir(plugindir):
                for f in os.listdir(plugindir):
                    basename, extension = os.path.splitext(f)
                    tgt = os.path.join(plugindir, f)

                    if extension == ".py":
                        self.plugins = imp.load_source("obj", tgt)

    def prepend_dir(self, dir):
        """Prepend a directory to the list of plugin directories.  After running,
        load_plugins() is called to maintain an up-to-datee list of plugins

        """

        if os.path.exists(dir):
            if self.plugin_dirs.count(dir) == 0:
                self.plugin_dirs.insert(0, dir)
                self.load_plugins()

    def append_dir(self, dir):
        """Append a directory to the list of plugin directories.  After running,
        load_plugins() is called to maintain an up-to-datee list of plugins

        """

        if os.path.exists(dir):
            if self.plugin_dirs.count(dir) == 0:
                self.plugin_dirs.append(dir)
                self.load_plugins()

    def get_plugin(self, plugin="", type=None):
        """Get a reference to the plugin.  The result may be then used to
        create new instances of that class or be executed as a function.

        Parameters:

        *plugin*
            The name of the plugin to get a reference for
        *type*
            The type of plugin to load (e.g., Cell, Action, ...).  If type is
            specified, matching plugins must be of the specified type.
            Otherwise, a PluginNotFoundError will be thrown.  If no type is
            specified, any plugin matching the given name will be acceptable.

        Example:
            obj_ref = get_plugin("MyObject")
            new_object = obj_ref()

        After this has executed, new_object will be an object of type MyObject.

        """

        try:
            ref = getattr(self.plugins, plugin)
        except AttributeError:
            raise PluginNotFoundError(plugin)
        else:
            if type != None and not issubclass(ref, type):
                raise PluginNotFoundError(plugin)
            return ref

    def plugin_exists(self, plugin=""):
        """Determine if a named plugin is present in the plugin directories"""
        return hasattr(self.plugins, plugin)
