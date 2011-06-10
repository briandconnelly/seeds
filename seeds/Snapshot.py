# -*- coding: utf-8 -*-
"""
Snapshots allow the state of the experiment (Experiment, Cells, Topologies, random
number generator) to be written to disk. This allows the experiment to be
re-started or extended.

It is important to note that open file handles (i.e., files open by an Action)
cannot be saved in the snapshot, so should a experiment be re-started using a
snapshot, new data files will be created.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

import pickle
import random
import copy
import time
import bz2

from seeds.ActionManager import *

class SnapshotObj(object):
    """
    SnapshotObjs contain the state of the Experiment and are used by the Snapshot
    class to store these important properties prior to being written to a
    file.

    Properties:
        experiment
            A reference to the Experiment object, which includes all configuration
            parameters, the Topologies, Cells, and Resources
        rstate
            The state of the pseudorandom number generator
        timestamp
            The current time
        format_version
            An integer representing the version of this object, should
            this class be added/removed/modified in future revisions.

    """

    def __init__(self):
        """Initialize the SnapshotObj"""
        self.experiment = None
        self.rstate = None
        self.timestamp = None
        self.format_version = 1

    def update(self, experiment):
        # Neither copy nor pickle can deal with the csv writer in the stats manager, so
        # back it up, temporarily disable it, copy the experiment, then restore it
        ambackup = experiment.action_manager
        pmbackup = experiment.plugin_manager

        experiment.action_manager = None
        experiment.plugin_manager = None
        self.experiment = copy.deepcopy(experiment)

        experiment.action_manager = ambackup
        experiment.plugin_manager = pmbackup

        self.rstate = random.getstate()
        self.timestamp = time.time()

class Snapshot(object):
    """
    The Snapshot class provides the functionality for creating, updating,
    writing, and restoring the state of experiments.  The intent is to allow
    the state of the experiment to be saved for analysis or to be used to re-start
    or extend experiments.

    Properties:

    so
        A SnapshotObj used to store the state of the experiment

    """

    def __init__(self):
        """Initialize a Snapshot instance"""
        self.so = SnapshotObj()

    def __str__(self):
        """Produce a string to be used when an Action object is printed"""
        return "Snapshot Object (Created: %s)" % (self.timestamp)

    def update(self, experiment):
        """Update the Snapshot's view of the Experiment"""
        self.so.update(experiment)

    def write(self, filename='snapshot'):
        """ Write the snapshot to a file.
        Parameters:

        *filename*
            Base name of the file to be written.  Will result as
            <filename>-<epoch>.snp

        """

        data_file = '%s-%06d.snp' % (filename, self.so.experiment.epoch)
        outfile = bz2.BZ2File(data_file, 'wb')
        pickle.dump(self.so, outfile)
        outfile.close()

    def read(self, filename='default'):
        """Read the given snapshot file (does not apply it to the experiment)"""
        infile = bz2.BZ2File(filename, 'rb')
        self.so = pickle.load(infile)
        infile.close()

    def apply(self, experiment):
        """ Apply the current snapshot to the experiment.  This sets the
        Experiment and the state of the pseudorandom number generator.
        
        Actions aren't resumed.  Once this is executed, a new ActionManager is
        initialized.  The data directory will be backed up, and a new one will
        be created.  Any actions currently running that write data to files
        will place the output in the new data directory.

        Similarly, the plugin manager will have to be re-loaded.  This should only
        impact the experiment if plugins used in the initial experiment are not
        available at the time the snapshot is loaded.

        Parameters:

        *experiment*
            A reference to the Experiment
        
        """

        if self.so.format_version == 1:
            # TODO: not all config values should be transfer.  How to specifiy?
            # - flag in config to say whether or not default has been used.  if not, don't use??

            random.setstate(self.so.rstate)

            experiment.config = self.so.experiment.config
            experiment.epoch = self.so.experiment.epoch
            experiment.topology_manager = self.so.experiment.topology_manager

            experiment.plugin_manager = PluginManager(experiment)
            experiment.action_manager = ActionManager(experiment)

            experiment.proceed = True

        else:
            print "Error: Unsupported Snapshot format"


