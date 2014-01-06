#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to perform a SEEDS experiment.  For more information, run with the
--help argument.  Plugin directories can be specified in the configuration as
well as in the $SEEDSPLUGINPATH environment variable, which allows for a user-
or system-wide repository of plugins.
"""

__author__ = "Brian Connelly <bdc@bconnelly.net>"
__version__ = "1.0.13"
__credits__ = "Brian Connelly"

import seeds as S
from seeds.SEEDSError import *

import argparse
import os
import re
import sys


class ProgressBar:
    def __init__(self, min_value=0, max_value=0, increment=1, width=80):
        self.min_value = min_value
        self.max_value = max_value
        self.increment = 1
        self.width = width
        self.amount = 0

        self.span = self.max_value - self.min_value
        self.epoch_maxstrlen  = len("epoch: %d" % (self.max_value))

    def update(self, value=None):
        if value:
            self.amount = value
        else:
            self.amount += self.increment

    def __str__(self):
        if self.span > 0:
            usable_width = self.width - self.epoch_maxstrlen - 2 - 1
            tick_width = usable_width / 100.0

            diff = float(self.amount - self.min_value)
            percent_done = int(round((diff / float(self.span)) * 100.0))
            num_ticks = int(round((percent_done * usable_width) / 100))

            return "[%s%s] epoch: %d" % ('#' * num_ticks, ' ' * (usable_width - num_ticks), self.amount)
        else:
            return "epoch: %d" % (self.amount)

def main():
    parser = argparse.ArgumentParser(prog='runseeds.py',
                                      description='Run an experiment using SEEDS')
    parser.add_argument("-c", "--config", default="seeds.cfg",
                        help="read config file (default: seeds.cfg)")
    parser.add_argument("-C", "--genconfig", action="store_true",
                        help="write config file used (experiment.cfg)")
    parser.add_argument("-d", "--data_dir", default="data",
                        help="write data to this directory (default: data)")
    parser.add_argument("-e", "--experiment", default=None,
                        help="label of the experiment to run")
    parser.add_argument("-p", "--param", action="append",
                        help="Set config values. Semicolon-separated list of section.param=val")
    parser.add_argument("-q", "--quiet", action="store_true", help="suppress all output messages")
    parser.add_argument("-s", "--seed", type=int, default=0,
                        help="set random seed (default: use clock)")
    parser.add_argument("--version", action="version",
                        version="%s (SEEDS Version %s)" % (__version__, S.__version__))
    cmd_args = parser.parse_args()

    if cmd_args.seed > 0:
        random_seed = cmd_args.seed
    else:
        random_seed=-1

    # Create the Experiment...
    try:
        experiment = S.Experiment(configfile=cmd_args.config, seed=random_seed,
                                  label=cmd_args.experiment)
    except SEEDSError as err:
        print("Error: %s" % err)
        sys.exit(1)

    if cmd_args.data_dir:
        experiment.config.set(experiment.config_section, 'data_dir', cmd_args.data_dir)


    # Add command-line config options
    if cmd_args.param != None:
        for param_str in cmd_args.param:
            options = re.split("\s*;\s*", param_str)
            for opt in options:
                # This is perhaps not the best regexp for comma-separated lists as values... need spaces.
                m = re.match(r"(?P<section>[A-Za-z0-9:_]+)\.(?P<parameter>[A-Za-z0-9:_]+)\s*=\s*(?P<value>-?[A-Za-z0-9_\.\,]+)", opt)
                if m != None:
                    experiment.config.set(m.group("section"), m.group("parameter"), m.group("value"))
                else:
                    print("Error: Could not parse parameter setting", opt)

    # Get the current configured list of plugin directories
    cfg_plugindirs = experiment.config.get(section="Experiment", name="plugin_dirs")
    if cfg_plugindirs:
        plugindirs = experiment.config.get(section="Experiment", name="plugin_dirs").split(",")
    else:
        plugindirs = []

    # Add any plugin paths specified in the environment via $SEEDSPLUGINPATH
    # First, the directories in the configuration will be scanned, followed by
    # those specified in $SEEDSPLUGINPATH, followed by the SEEDS built-in
    # plugins.
    seedspluginpath = os.environ.get("SEEDSPLUGINPATH")
    if seedspluginpath != None and len(seedspluginpath) > 0:
        plugindirs += seedspluginpath.rsplit(":")

    if len(plugindirs) > 0:
        pdirs = ",".join(plugindirs)
        experiment.config.set(section="Experiment", name="plugin_dirs", value=pdirs)

    if not cmd_args.quiet:
        print("Experiment ID: %s" % experiment.uuid)

    # Set up a progress bar
    prog = ProgressBar(min_value = 0, max_value=experiment.config.getint(experiment.config_section, 'epochs', default=0))

    # Do the experiment...
    try:
        for epoch in experiment:
            prog.update()
            if not cmd_args.quiet:
                sys.stdout.write("%s\r" % prog)
                sys.stdout.flush()
    except SEEDSError as err:
        print("Error: %s" % err)
        sys.exit(2)
    else:
        experiment.teardown()

    # Write a config file
    if cmd_args.genconfig:
        experiment.config.write(filename='experiment.cfg')

    if not cmd_args.quiet:
        print("")

if __name__ == "__main__":
    main()

