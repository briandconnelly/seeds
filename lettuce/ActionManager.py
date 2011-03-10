"""
Manage and execute Action objects
"""

__author__ = "Luis Zaman <zamanlui@msu.edu>"
__version__ = "0.9.0"
__credits__ = "Luis Zaman, Brian Connelly"


import os
import shutil
import datetime

from lettuce.Action import *
from lettuce.World import *
import lettuce.action
from lettuce.action import *


class ActionManager(object):
    """
    Properties:

    data_dir
        Directory in which to write files.  From data_dir configuration
        parameter in [Experiment]
    actionSet
        Set of Action items to be executed

    Configuration:

    The ActionManager also looks for the configuration variable named
    'data_dir' in the [Experiment] block.  This value stores the name of the
    directory into which actions write data.

    """

    def __init__(self, world):
        """Initialize an ActionManager object

        Parameters:

        *world*
            A reference to the World

        """

        self.world = world

        data_dir = self.world.config.get('Experiment', 'data_dir', 'data')

        if os.path.exists(data_dir):
             newname = data_dir + '-' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
             shutil.move(data_dir, newname)
         
        os.mkdir(data_dir)

        self.actionSet = {}
        self.setup_actions()
            
    def setup_actions(self):
        """Gather a list of the Actions to be executed based on the [Actions]
        config block.

        """

        configItems = self.world.config.items('Actions')
        
        for item in configItems:
            self.actionSet[globals()[item[0]](self.world)] = item[1]
            
    def update(self):
        """Update each Action"""
        for action in self.actionSet:
            action.update()
        
