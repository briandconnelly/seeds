# -*- coding: utf-8 -*-
"""
Snapshots allow the state of the experiment (World, Cells, Topologies, random
number generator) to be written to disk. This allows the experiment to be
re-started or extended.

It is important to note that open file handles (i.e., files open by an Action)
cannot be saved in the snapshot, so should a experiment be re-started using a
snapshot, new data files will be created.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.1"
__credits__ = "Brian Connelly"

import pickle
import random
import copy
import time
import bz2
import os

class SnapshotObj(object):
    """
    SnapshotObjs contain the state of the world and are used by the Snapshot
    class to store these important properties prior to being written to a
    file.

    Properties:
        world
            A reference to the World object, which includes all configuration
            parameters, the Topologies (and therefore Cells and Resources)
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
        self.world = None
        self.rstate = None
        self.timestamp = None
        self.format_version = 1

    def update(self, world):
        # Neither copy nor pickle can deal with the csv writer in the stats manager, so
        # back it up, temporarily disable it, copy the world, then restore it
        ambackup = world.action_manager
        world.action_manager = None
        self.world = copy.deepcopy(world)
        world.action_manager = ambackup

        self.rstate = random.getstate()
        self.timestamp = time.time()

class Snapshot(object):
    """
    The Snapshot class provides the functionality for creating, updating,
    writing, and restoring the state of experiments.  The intent is to allow
    the state of the world to be saved for analysis or to be used to re-start
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

    def update(self, world):
        """Update the Snapshot's view of the world"""
        self.so.update(world)

    def write(self, filename='snapshot'):
        """ Write the snapshot to a file.
        Parameters:

        *filename*
            Base name of the file to be written.  Will result as
            <filename>-<epoch>.snp

        """

        filename = '%s-%06d.snp' % (filename, self.so.world.epoch)
        data_file = os.path.join(data_dir, filename)
        outfile = bz2.BZ2File(data_file, 'wb')
        pickle.dump(self.so, outfile)
        outfile.close()

    def read(self, filename='default'):
        """Read the given snapshot file (does not apply it to the experiment)"""
        infile = bz2.BZ2File(filename, 'rb')
        self.so = pickle.load(infile)
        infile.close()

    def apply(self, world):
        """ Apply the current snapshot to the experiment.  This sets the World,
        the state of the pseudorandom number generator, and the Actions.

        Parameters:

        *world*
            A reference to the World
        
        """
        # Make the current world the world of the snapshot and set the state of
        # the random number generator

        # TODO: should there be any checks to see if the worlds are compatible? 
        #       - this would be used to extend experiments or revert something.  big changes not likely (or assumed)
        # TODO: snapshot doesn't store the actionmanager, so do we keep the old stats manager?
        #       - simply re-initializing it will move the other files to backups.  is that what we want?

        world = self.so.world
        world.action_manager = ActionManager(self)
        random.setstate(self.so.rstate)

