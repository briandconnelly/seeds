# -*- coding: utf-8 -*-
""" Print detailed information about the Experiment and the software
environment under which the Experiment was performed.  This action is intended
to aide in recreating and reproducing Experiments.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

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

        Config file settings:
        [PrintExperimentInformation]
        epoch_start = 0    Epoch at which to start writing (default 0)
        epoch_end = 0      Epoch at which to stop writing (default 0)
        frequency = 1      Frequency (epochs) to write.  In this example, we write every other epoch.  (default 1)
        priority = 0       Priority of this Action.  Higher priority Actions run first. (default 0)
        filename = information  Filename to be written to

    """

    def __init__(self, experiment):
        """Initialize the PrintExperimentInformation Action"""

        super(PrintExperimentInformation, self).__init__(experiment)
        self.epoch_start = self.experiment.config.getint('PrintExperimentInformation', 'epoch_start', default=0)
        self.epoch_end = self.experiment.config.getint('PrintExperimentInformation', 'epoch_end', default=0)
        self.frequency = self.experiment.config.getint('PrintExperimentInformation', 'frequency', default=1)
        self.priority = self.experiment.config.getint('PrintExperimentInformation', 'priority', default=0)
        self.filename = self.experiment.config.get('PrintExperimentInformation', 'filename', 'information')
        self.name = "PrintExperimentInformation"

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        full_filename = "%s.txt" % (self.filename)
        data_file = self.datafile_path(full_filename)
        f = open(data_file, 'w')
        f.write('SEEDS Experiment Information:\n\n')
        f.write('Experiment UUID: %s\n' % (self.experiment.uuid))
        f.write('Configuration File: %s\n' % (self.experiment.config.filename))
        sha1_checksum = hashlib.sha1(file(self.experiment.config.filename, 'rb').read()).hexdigest()
        f.write('Configuration File SHA-1 Checksum: %s\n' % (sha1_checksum))
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

