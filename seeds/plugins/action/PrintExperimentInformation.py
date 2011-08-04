# -*- coding: utf-8 -*-
""" Print detailed information about the Experiment and the software
environment under which the Experiment was performed.  This action is intended
to aide in recreating and reproducing Experiments.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import datetime
import hashlib
import networkx as nx
import os
import seeds as s
import sys

from seeds.Action import *
from seeds.SEEDSError import *


class PrintExperimentInformation(Action):
    """ Write detailed information about the Experiment and the software
    environment under which it was performed.  Generally, this Action only
    needs to be run once per experiment.

    Configuration parameters for this action are set in the
    [PrintExperimentInformation] section.

    Configuration Options:

    epoch_start
        The epoch at which to start executing (default: 0)
    epoch_end
        The epoch at which to stop executing (default: end of experiment)
    frequency
        The frequency (epochs) at which to execute (default: 1)
    priority
        The priority of this action.  Actions with higher priority get run
        first.  (default: 0)
    filename
        Name of the file to be written to (default: information.txt)

    Configuration Example:

    [PrintExperimentInformation]
    epoch_start = 0
    epoch_end = 0
    frequency = 1
    priority = 0
    filename = information.txt

    """

    def __init__(self, experiment, label=None):
        """Initialize the PrintExperimentInformation Action"""

        super(PrintExperimentInformation, self).__init__(experiment,
                                                         name="PrintExperimentInformation",
                                                         label=label)

        self.epoch_start = self.experiment.config.getint(self.config_section, 'epoch_start', default=0)
        self.epoch_end = self.experiment.config.getint(self.config_section, 'epoch_end', default=0)
        self.frequency = self.experiment.config.getint(self.config_section, 'frequency', default=1)
        self.priority = self.experiment.config.getint(self.config_section, 'priority', default=0)
        self.filename = self.experiment.config.get(self.config_section, 'filename', 'information.txt')
        self.name = "PrintExperimentInformation"

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        data_file = self.datafile_path(self.filename)
        f = open(data_file, 'w')
        f.write('SEEDS Experiment Information:\n\n')
        f.write('Date and Time (UTC): %s\n' % (datetime.datetime.utcnow()))
        f.write('Experiment UUID: %s\n' % (self.experiment.uuid))
        f.write('Configuration File: %s\n' % (self.experiment.config.filename))

        sha256_checksum = hashlib.sha256()
        config_file = open(self.experiment.config.filename, 'rb')
        sha256_checksum.update(config_file.read())
        f.write('Configuration File SHA-256 Checksum: %s\n' % (sha256_checksum.hexdigest()))

        f.write('User Name: %s\n' % (os.getlogin()))
        f.write('Command Line: %s\n' % (sys.argv))
        f.write('Process ID: %d\n' % (os.getpid()))
        f.write('SEEDS Version: %s\n' % (s.__version__))
        f.write('NetworkX Version: %s\n' % (nx.__version__))
        f.write('Python Version: %s\n' % (sys.version))
        f.write('Platform: %s\n' % (sys.platform))
        f.write('Executable: %s\n' % (sys.executable))
        f.write('Exec Prefix: %s\n' % (sys.exec_prefix))
        f.write('Path: %s\n' % (sys.path))
        f.write('Modules: %s\n' % (sys.modules))
        f.write('Environment: %s\n' % (os.environ))
        f.close()

