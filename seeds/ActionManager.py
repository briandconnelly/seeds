# -*- coding: utf-8 -*-
"""
Manage Action objects

If a configured Action is not part of the standard SEEDS list, the plugin
manager will be used to see if it has been defined by the user.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly, Luis Zaman"

import datetime
import heapq
import os
import shutil

from seeds.Action import *
from seeds.PluginManager import *


class ActionManager(object):
    """Manage the creation and execution of a set of Actions

    Attributes:

    actions
        The list of Action objects to be run
    action_names
        A list of Actions and their labels that are being executed.

    """

    def __init__(self, experiment):
        """Initialize the ActionManager

        Parameters:

        *experiment*
            A reference to the Experiment

        """

        self.experiment = experiment

        data_dir = self.experiment.config.get(section=self.experiment.config_section,
                                              name='data_dir',
                                              default='data')

        if os.path.exists(data_dir):
            newname = data_dir + '-' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            shutil.move(data_dir, newname)

        os.mkdir(data_dir)

        self.actions = []
        self.action_names = []
        self.setup_actions()

    def setup_actions(self):
        """Initialize and set up the list of Actions to be executed"""

        actionstring = self.experiment.config.get(section=self.experiment.config_section,
                                             name='actions', default="")

        if not actionstring:
            return

        actionlist = [action.strip() for action in actionstring.split(',')]

        for item in actionlist:
            parsed = item.split(':')
            action = parsed[0]

            if len(parsed) > 1:
                label = parsed[1]
            else:
                label = None

            try:
                oref = self.experiment.plugin_manager.get_plugin(action, type=Action)
                a = oref(self.experiment, label=label)
                self.add_action(a)
            except PluginNotFoundError as err:
                raise ActionPluginNotFoundError(action)
            except SEEDSError as err:
                raise SEEDSError(err)

    def add_action(self, action):
        """Add an Action to the list of actions to be scheduled.

        Parameters:

        *action*
            An instantiated Action object

        """

        if action.config_section in self.action_names:
            print "Warning: Action '%s' listed twice.  Skipping duplicates." % (action.config_section)
        else:
            heapq.heappush(self.actions, (action.priority, action))
            self.action_names.append(action.config_section)

    def action_loaded(self, name):
        """ Determine whether or not a given action is being used.  Useful for
        having prerequisite Actions.

        Parameters:

        *name*
            The name of an Action to be searched for

        """

        return self.get_loaded_actions().count(name) > 0

    def get_loaded_actions(self):
        """ Return a list of the names of loaded Actions """
        return [action.name for (priority, action) in self.actions]

    def update(self):
        """Update all actions"""
        [a.update() for (p,a) in sorted(self.actions, reverse=True)]

    def teardown(self):
        """Clean up after all actions at the end of an experiment"""
        [a.teardown() for (p,a) in sorted(self.actions, reverse=True)]

