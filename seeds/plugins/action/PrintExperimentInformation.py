# -*- coding: utf-8 -*-
""" Print detailed information about the experiment and the software
environment under which it was performed. This action is intended to aide in
recreating and reproducing experiments.
"""

__author__ = "Brian Connelly <bdc@bconnelly.net>"
__credits__ = "Brian Connelly"


import datetime
import hashlib
import json
import os
import pwd
import sys

import networkx as nx
import seeds as s

from seeds.Action import *
from seeds.Plugin import *


class PrintExperimentInformation(Action, Plugin):
    """ Write detailed information about the experiment and the software
    environment under which it was performed.  Generally, this action only
    needs to be run once per experiment.

    Configuration is done in the [PrintExperimentInformation] section

    Configuration Options:

    epoch_start
        The epoch at which to start executing. Although epoch_start defaults to
        0 in most actions, this action defaults to 1 so that most other plugins
        have run first, enabling configuration values printed by this action to
        also show default values used (default: 1).
    epoch_end
        The epoch at which to stop executing (default: end of experiment)
    frequency
        The frequency (epochs) at which to execute (default: 1)
    priority
        The priority of this action.  Actions with higher priority get run
        first. (default: 0)
    outfile
        The name of the file to write (default: 'experiment_information.json')


    Configuration Example:

    [PrintExperimentInformation]
    epoch_start = 1
    epoch_end = 1
    frequency = 1
    priority = 0
    outfile = experiment_info.json

    """

    __name__ = "PrintExperimentInformation"
    __version__ = (1,0)
    __author__ = "Brian Connelly <bdc@bconnelly.net>"
    __credits__ = "Brian Connelly"
    __description__ = "Write detailed information about the experiment and the software environment under which it was performed"
    __type__ = 4        
    __requirements__ = [] 

    def __init__(self, experiment, label=None):
        """Initialize the PrintExperimentInformation Action"""

        super(PrintExperimentInformation, self).__init__(experiment,
                                                         name="PrintExperimentInformation",
                                                         label=label)

        self.epoch_start = self.experiment.config.getint(self.config_section, 'epoch_start', 1)
        self.epoch_end = self.experiment.config.getint(self.config_section, 'epoch_end', default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint(self.config_section, 'frequency', 1)
        self.priority = self.experiment.config.getint(self.config_section, 'priority', 0)
        self.outfile = self.experiment.config.get(self.config_section, 'outfile', 'experiment_information.json')

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        information = {}
        information['UUID'] = str(self.experiment.uuid)
        information['date_UTC'] = str(datetime.datetime.utcnow())
        information['command_line'] = sys.argv

        # System information
        system = {}
        system['platform'] = sys.platform
        system['process_id'] = os.getpid()
        system['username'] = os.getlogin()
        system['uid'] = os.geteuid()
        system['gid'] = os.getgid()
        system['username'] = pwd.getpwuid(system['uid'])[0]
        system['cwd'] = os.getcwd()
        system['environment'] = {k:v for k,v in os.environ.items()}
        
        pyinfo = {}
        pyinfo['version'] = sys.version
        pyinfo['prefix'] = sys.prefix
        pyinfo['executable'] = sys.executable
        pyinfo['exec_prefix'] = sys.exec_prefix
        pyinfo['flags'] = str(sys.flags)
        pyinfo['path'] = sys.path
        pyinfo['byte_order'] = sys.byteorder
        pyinfo['float_info'] = str(sys.float_info)
        system['python'] = pyinfo
        information['system'] = system

        # SEEDS information
        seeds = {}
        seeds['version'] = s.__version__
        seeds['plugins'] = []

        for p in self.experiment.plugin_manager.list_plugins():
            plugin = {'name': p, 'version': self.experiment.plugin_manager.get_plugin(p).__version__} 
            seeds['plugins'].append(plugin)

        information['SEEDS'] = seeds

        # NetworkX information
        networkx = {}
        networkx['version'] = nx.__version__
        information['NetworkX'] = networkx

        # Configuration file stuff
        configuration = {}
        configuration['file'] = self.experiment.config.filename

        sha256_checksum = hashlib.sha256()
        config_file = open(self.experiment.config.filename, 'rb')
        sha256_checksum.update(config_file.read())

        configuration['checksum'] = sha256_checksum.hexdigest()

        sections = {}
        for sec in self.experiment.config.config.sections():
            opts = {}
            for o in self.experiment.config.config.options(sec):
                opts[o] = self.experiment.config.get(sec, o)
            sections[sec] = opts
        configuration['sections'] = sections
        information['configuration'] = configuration

        data_file = self.datafile_path(self.outfile)
        json.dump(information, open(data_file, 'w'), indent=True)

