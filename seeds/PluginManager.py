# -*- coding: utf-8 -*-
"""
Manage plugins for the system

Plugins allow SEEDS to be extended to suit the needs of users without adding
to the base code and adding additional dependencies.  Examples include
additional Cells, Topologies, or Actions.  Plugins may be stored in multiple
directories.
"""

__author__ = "Brian Connelly <bdc@bconnelly.net>"
__credits__ = "Brian Connelly"


import imp
import inspect
import os
import sys

from seeds.Action import *
from seeds.Cell import *
from seeds.Plugin import *
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

        # Reverse the list of plugin directories so that when two plugins exist
        # with the same name, priority is given to the one earlier in the
        # (original) list
        pdirs = list(self.plugin_dirs)
        pdirs.reverse()

        for plugindir in pdirs:
            if os.path.exists(plugindir) and os.path.isdir(plugindir):
                for f in os.listdir(plugindir):
                    basename, extension = os.path.splitext(f)

                    if basename == "__init__" or extension != ".py":
                        continue

                    tgt = os.path.join(plugindir, f)
                    self.plugins = imp.load_source("obj", tgt)

    def prepend_dir(self, d):
        """Prepend a directory to the list of plugin directories.  After running,
        load_plugins() is called to maintain an up-to-date list of plugins

        Parameters:

        *d*
            The directory to prepend

        """

        if os.path.exists(d):
            if self.plugin_dirs.count(d) == 0:
                self.plugin_dirs.insert(0, d)
                self.load_plugins()

    def append_dir(self, d):
        """Append a directory to the list of plugin directories.  After running,
        load_plugins() is called to maintain an up-to-date list of plugins

        Parameters:

        *d*
            The directory to append

        """

        if os.path.exists(d):
            if self.plugin_dirs.count(d) == 0:
                self.plugin_dirs.append(d)
                self.load_plugins()

    def plugin_exists(self, plugin=""):
        """Determine if a named plugin is present in the plugin directories"""
        return hasattr(self.plugins, plugin)

    def get_plugin(self, plugin="", type=None, version=None, version_operator='='):
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
        *version*
            Tuple describing the desired version to load.  If not defined, any
            version will be accepted. (default: None).
        *version_operator*

            When a version tuple is specified, the operator to compare
            candidate plugin versions with.  One of:

            <  : The plugin must be less than the specified version
            <= : The plugin version must be less than or equal to the specified
                 version
            =  : The plugin version must exactly match the specified version
                 (default)
            >= : The plugin version must be greater than or equal to the
                 specified version
            >  : The plugin version must be greater than the specified version

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
            elif version != None:
                cmp_val = ref.cmp_version(version)

                if version_operator == '<' and cmp_val != -1:
                    raise PluginVersionNotFoundError(plugin, version)
                elif version_operator == '<=' and cmp_val == 1:
                    raise PluginVersionNotFoundError(plugin, version)
                elif version_operator == '=' and cmp_val != 0:
                    raise PluginVersionNotFoundError(plugin, version)
                elif version_operator == '>=' and cmp_val == -1:
                    raise PluginVersionNotFoundError(plugin, version)
                elif version_operator == '>' and cmp_val != 1:
                    raise PluginVersionNotFoundError(plugin, version)
                else:
                    # Just in case something weird happens, catch it
                    raise PluginVersionNotFoundError(plugin, version)

            return ref

    def get_topology_plugin(self, plugin=None, version=None, version_operator='='):
        """Get a reference to specified Topology plugin.  The result may be
        then used to create new instances of that class or be executed as a
        function.

        Parameters:

        *plugin*
            The name of the plugin to get a reference for
        *version*
            Tuple describing the desired version to load.  If not defined, any
            version will be accepted. (default: None).
        *version_operator*

            When a version tuple is specified, the operator to compare
            candidate plugin versions with.  One of:

            <  : The plugin must be less than the specified version
            <= : The plugin version must be less than or equal to the specified
                 version
            =  : The plugin version must exactly match the specified version
                 (default)
            >= : The plugin version must be greater than or equal to the
                 specified version
            >  : The plugin version must be greater than the specified version

        After this has executed, new_object will be an object of type MyObject.
        """

        try:
            return self.get_plugin(plugin, type=Topology, version=version, version_operator=version_operator)
        except PluginNotFoundError as err:
            raise TopologyPluginNotFoundError(plugin)

    def get_cell_plugin(self, plugin=None, version=None, version_operator='0'):
        """Get a reference to specified Cell plugin.  The result may be then
        used to create new instances of that class or be executed as a
        function.

        Parameters:

        *plugin*
            The name of the plugin to get a reference for
        *version*
            Tuple describing the desired version to load.  If not defined, any
            version will be accepted. (default: None).
        *version_operator*

            When a version tuple is specified, the operator to compare
            candidate plugin versions with.  One of:

            <  : The plugin must be less than the specified version
            <= : The plugin version must be less than or equal to the specified
                 version
            =  : The plugin version must exactly match the specified version
                 (default)
            >= : The plugin version must be greater than or equal to the
                 specified version
            >  : The plugin version must be greater than the specified version

        After this has executed, new_object will be an object of type MyObject.
        """

        try:
            return self.get_plugin(plugin, type=Cell, version=version, version_operator=version_operator)
        except PluginNotFoundError as err:
            raise CellPluginNotFoundError(plugin)


    def get_action_plugin(self, plugin=None, version=None, version_operator='='):
        """Get a reference to specified Action plugin.  The result may be then
        used to create new instances of that class or be executed as a
        function.

        Parameters:

        *plugin*
            The name of the plugin to get a reference for
        *version*
            Tuple describing the desired version to load.  If not defined, any
            version will be accepted. (default: None).
        *version_operator*

            When a version tuple is specified, the operator to compare
            candidate plugin versions with.  One of:

            <  : The plugin must be less than the specified version
            <= : The plugin version must be less than or equal to the specified
                 version
            =  : The plugin version must exactly match the specified version
                 (default)
            >= : The plugin version must be greater than or equal to the
                 specified version
            >  : The plugin version must be greater than the specified version

        After this has executed, new_object will be an object of type MyObject.
        """

        try:
            return self.get_plugin(plugin, type=Action, version=version, version_operator=version_operator)
        except PluginNotFoundError as err:
            raise ActionPluginNotFoundError(plugin)


    def get_resource_cell_plugin(self, plugin=None, version=None, version_operator='='):
        """Get a reference to specified ResourceCell plugin.  The result may be
        then used to create new instances of that class or be executed as a
        function.

        Parameters:

        *plugin*
            The name of the plugin to get a reference for
        *version*
            Tuple describing the desired version to load.  If not defined, any
            version will be accepted. (default: None).
        *version_operator*

            When a version tuple is specified, the operator to compare
            candidate plugin versions with.  One of:

            <  : The plugin must be less than the specified version
            <= : The plugin version must be less than or equal to the specified
                 version
            =  : The plugin version must exactly match the specified version
                 (default)
            >= : The plugin version must be greater than or equal to the
                 specified version
            >  : The plugin version must be greater than the specified version

        After this has executed, new_object will be an object of type MyObject.
        """

        try:
            return self.get_plugin(plugin, type=ResourceCell, version=version, version_operator=version_operator)
        except PluginNotFoundError as err:
            raise ResourceCellPluginNotFoundError(plugin)


    def list_plugins(self):
        mylist = []

        for p in dir(self.plugins):
            ref = getattr(self.plugins, p)

            if inspect.isclass(ref) and issubclass(ref, Plugin):
                mylist.append(p)

        return mylist
