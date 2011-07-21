# -*- coding: utf-8 -*-
""" Actions to deal with Snapshot files
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from seeds.Action import *


class WriteSnapshot(Action):
    """ Write a Snapshot file

    Configuration is done in the [WriteSnapshot] section

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
    write_on_end
        Whether or not to write a Snapshot at the end of the run, regardless of
        whether the epoch is beyond the epoch_end parameter value.
    filename
        Base name for files.  The epoch at which the file was created will also
        comprise the resulting file name.  For example, a filename of
        'snapshot' when run at epoch 1200 would produce the file
        snapshot-001200.snp.  (default: 'snapshot')


    Configuration Example:

    [WriteSnapshot]
    epoch_start = 3
    epoch_end = 100
    frequency = 2
    priority = 0
    filename = snapshot
    write_on_end = True

    """

    def __init__(self, experiment, label=None):
        """Initialize the WriteSnapshot Action"""

        super(WriteSnapshot, self).__init__(experiment,
                                            name="WriteSnapshot",
                                            label=label)

        self.epoch_end = self.experiment.config.getint(self.config_section, 'epoch_end', default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint(self.config_section, 'frequency', 1)
        self.priority = self.experiment.config.getint(self.config_section, 'priority', 0)
        self.filename = self.experiment.config.get(self.config_section, 'filename', 'snapshot')
        self.write_on_end = self.experiment.config.getboolean(self.config_section, 'write_on_end', default=True)
        self.name = "WriteSnapshot"

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        data_file = self.datafile_path(self.filename)
        self.experiment.get_snapshot().write(data_file)

    def teardown(self):
        """Perform cleanup.  If user requests a snapshot to be written at the
        end of an experiment, do so.  This is useful if the experiment ends
        before a predefined number of epochs, as would be the case with Actions
        such as StopOnConvergence

        """

        if self.write_on_end:
            data_file = self.datafile_path(self.filename)
            self.experiment.get_snapshot().write(data_file)

