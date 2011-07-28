#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to perform a SEEDS experiment.  For more information, run with the
--help argument.  Plugin directories can be specified in the configuration as
well as in the $SEEDSPLUGINPATH environment variable, which allows for a user-
or system-wide repository of plugins.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "1.0.8"
__credits__ = "Brian Connelly"

import seeds as S
from seeds.SEEDSError import *
from optparse import OptionParser

import os
import re
import sys


class ProgressBar:
    def __init__(self, min_value = 0, max_value = 0, width=60):
        self.bar = ''
        self.min = min_value
        self.max = max_value
        self.width = width
        self.amount = 0       # When amount == max, we are 100% done
        self.update_amount(0)

    def update_amount(self, new_amount = None):
        """
        Update self.amount with 'new_amount', and then rebuild the bar
        string.
        """
        if not new_amount: new_amount = self.amount
        if new_amount < self.min: new_amount = self.min
        if new_amount > self.max: new_amount = self.max
        self.amount = new_amount
        self.build_bar()

    def build_bar(self):
        """
        Figure new percent complete, and rebuild the bar string base on
        self.amount.
        """
        diff = float(self.amount - self.min)
        span = self.max - self.min
        percent_done = int(round((diff / float(span)) * 100.0))

        # figure the proper number of 'character' make up the bar
        all_full = self.width - 2
        num_hashes = int(round((percent_done * all_full) / 100))

        # build a progress bar with self.char and spaces (to create a
        # fixed bar (the percent string doesn't move)
        percent_str = "epoch: " + str(self.amount)
        self.bar = '#' * num_hashes + ' ' * (all_full-num_hashes)
        self.bar = '[' + self.bar + '] ' + percent_str

    def __str__(self):
        return str(self.bar)


def main():
    parser = OptionParser('usage: %prog [options] arg')
    parser.add_option("-c", "--config", dest="configfile", type="string", default="seeds.cfg",
                      help="read config file (default: seeds.cfg)")
    parser.add_option("-C", "--genconfig", action="store_true", dest="genconfig", help="write config file used (experiment.cfg)")
    parser.add_option("-d", "--data_dir", dest="datadir", type="string",
                      help="write data to this directory (default: data)")
    parser.add_option("-e", "--experiment", dest="experiment", type="string", help="label of the experiment to run")
    parser.add_option("-p", "--param", dest="params", type="string", help="Set config values.  Semicolon-separated list of section.param=val")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet", help="suppress all output messages")
    parser.add_option("-s", "--seed", dest="seed", type=int, default=0,
                      help="set random seed (default: use clock)")
    parser.add_option("-v", "--version", action="store_true", dest="version", help="display version information and quit")

    (cmd_options, cmd_args) = parser.parse_args()

    if cmd_options.seed > 0:
        random_seed = cmd_options.seed
    else:
        random_seed=-1

    if cmd_options.version:
        print "%s (SEEDS Version %s)" % (__version__, S.__version__)
        sys.exit(0)

    if cmd_options.experiment:
        experiment_label = cmd_options.experiment
    else:
        experiment_label = None

    # Create the Experiment...
    try:
        experiment = S.Experiment(configfile=cmd_options.configfile, seed=random_seed,
                                  label=experiment_label)
    except SEEDSError as err:
        print "Error:", err
        sys.exit(1)

    if cmd_options.datadir:
        experiment.config.set(experiment.config_section, 'data_dir', cmd_options.datadir)


    # Add command-line config options
    if cmd_options.params != None:
        options = re.split("\s*;\s*", cmd_options.params)
        for opt in options:
            # This is perhaps not the best regexp for comma-separated lists as values... need spaces.
            m = re.match(r"(?P<section>[A-Za-z0-9:_]+)\.(?P<parameter>[A-Za-z0-9:_]+)\s*=\s*(?P<value>-?[A-Za-z0-9_\.\,]+)", opt)
            if m != None:
                experiment.config.set(m.group("section"), m.group("parameter"), m.group("value"))
            else:
                print "Error: Could not parse parameter setting", opt

    # Get the current configured list of plugin directories
    cfg_plugindirs = experiment.config.get(section="Experiment", name="plugin_dirs")
    if cfg_plugindirs:
        plugindirs = experiment.config.get(section="Experiment", name="plugin_dirs").split(",")
    else:
        plugindirs = []

    # Add any plugin paths specified in the environment via $SEEDSPLUGINPATH
    seedspluginpath = os.environ.get("SEEDSPLUGINPATH")
    if seedspluginpath != None and len(seedspluginpath) > 0:
        for p in seedspluginpath.rsplit(":"):
            pdir = os.path.expanduser(p)
            plugindirs.append(pdir)

    if len(plugindirs) > 0:
        pdirs = ",".join(plugindirs)
        experiment.config.set(section="Experiment", name="plugin_dirs", value=pdirs)

    if not cmd_options.quiet:
        print "Experiment ID:", experiment.uuid

    # Set up a progress bar
    prog = ProgressBar(0, experiment.config.getint(experiment.config_section, 'epochs'))
    oldprog = str(prog)

    # Do the experiment...
    try:
        for epoch in experiment:
            prog.update_amount(epoch)
            if not cmd_options.quiet and oldprog != str(prog):
                print prog, "\r",
                sys.stdout.flush()
                oldprog=str(prog)
    except SEEDSError as err:
        print "Error:", err
        sys.exit(2)
    else:
        experiment.teardown()

    # Write a config file
    if cmd_options.genconfig:
        experiment.config.write(filename='experiment.cfg')

    if not cmd_options.quiet:
        print

if __name__ == "__main__":
    main()

