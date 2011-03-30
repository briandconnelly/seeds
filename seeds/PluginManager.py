# -*- coding: utf-8 -*-
"""
Manage plugins for the system

Plugins allow SEEDS to be extended to suit the needs of users without adding
to the base code and adding additional dependencies.  Examples include
additional Cells, Topologies, or Actions.  Plugins may be stored in multiple
directories.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.1"
__credits__ = "Brian Connelly"


import imp
import os
import sys

class PluginManager(object):
    """ The PluginManager object keeps track of plugins in the specified plugin
    directories and allows users to query these plugins and receive references
    to the resulting objects.

    Properties:

    world
        A reference to the World
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

    def __init__(self, world):
        """Initialize a PluginManager object

        Parameters:

        *world*
            A reference to the World

        """

        self.world = world
        self.plugin_dirs = []
        self.plugins = None

        plugindirs = self.world.config.get(section='Experiment', name='plugin_dirs', default="")
        if len(plugindirs) > 0:
            for d in plugindirs.split(','):
                if os.path.exists(d):
                    self.plugin_dirs.append(d)

        self.load_plugins()

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
                    elif extension == ".pyc":
                        self.plugins = imp.load_compiled("obj", tgt)

    def add_dir(self, dir):
        """Add a directory to the list of plugin directories.  After running,
        load_plugins() is called to maintain an up-to-datee list of plugins

        """

        if os.path.exists(dir):
            self.plugin_dirs.append(dir)
            self.load_plugins()

    def get_plugin(self, plugin=""):
        """Get a reference to the plugin.  The result may be then used to
        create new instances of that class or be executed as a function.

        Example:

        obj_ref = get_plugin("MyObject")
        new_object = obj_ref()

        After this has executed, new_object will be an object of type MyObject.

        """

        try:
            ref = getattr(self.plugins, plugin)
            return ref
        except AttributeError:
            return None

    def plugin_exists(self, plugin=""):
        """Determine if a named plugin is present in the plugin directories"""
        try:
            ref = getattr(self.plugins, plugin)
            return True
        except AttributeError:
            return False

