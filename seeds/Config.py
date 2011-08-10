# -*- coding: utf-8 -*-
"""
Handle configurations for experiments

The values stored in a configuration can be read from a file, specified on the
command line or through GUI elements, or set by code elements.  These
configuration values can then be queried or updated.

"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly, Luis Zaman"

import datetime
import os
import re
import sys

if sys.version_info[0] == 3:
    import configparser
    NO_SECTION_ERROR = configparser.NoSectionError
    NO_OPTION_ERROR = configparser.NoOptionError
else:
    import ConfigParser
    NO_SECTION_ERROR = ConfigParser.NoSectionError
    NO_OPTION_ERROR = ConfigParser.NoOptionError

import seeds as S

class Config(object):
    """A Config object contains the configuration for an experiment.  The
    values in a configuration can be queried and also updated.
    
    """

    def __init__(self, experiment, filename=None):
        """Initialize a Config object

        If an input file is provided, the configuration will be read from this.
        Otherwise, an empty Config is created, and Experiment will need to use
        either default values or values provided through the command line or
        GUI program.

        Named Parameters:

        *experiment*
            A pointer to the Experiment
        *filename*
            The name of the configuration to read from

        """
        self.experiment = experiment

        if sys.version_info[0] == 3:
            self.config = configparser.SafeConfigParser()
        else:
            self.config = ConfigParser.SafeConfigParser()

        self.config.optionxform = str
        self.filename = os.path.abspath(filename)

        if filename != None:
            self.config.read(filename)

        self.resource_sections = []
        for sec in self.config.sections():
            match = re.match("Resource:([a-zA-Z_]+)", sec)
            if match != None:
                self.resource_sections.append(sec)

    def get(self, section, name, default=None):
        """Get a configured value for a variable

        Parameters:

        *section*
            The section under which the variable is defined
        *name*
            The name of the variable
        *default*
            The value to use should the variable not be defined

        """

        try:
            val = self.config.get(section, name)
        except NO_SECTION_ERROR:
            self.config.add_section(section)
            self.config.set(section, name, str(default))
            val = default
        except NO_OPTION_ERROR:
            self.config.set(section, name, str(default))
            val = default
        return val

    def getint(self, section, name, default=None):
        """Get a configured integer value for a variable

        Parameters:

        *section*
            The section under which the variable is defined
        *name*
            The name of the variable
        *default*
            The value to use should the variable not be defined

        """

        try:
            val = self.config.getint(section, name)
        except NO_SECTION_ERROR:
            self.config.add_section(section)
            self.config.set(section, name, str(default))
            val = default
        except NO_OPTION_ERROR:
            self.config.set(section, name, str(default))
            val = default
        return val

    def getfloat(self, section, name, default=None):
        """Get a configured floating point value for a variable

        Parameters:

        *section*
            The section under which the variable is defined
        *name*
            The name of the variable
        *default*
            The value to use should the variable not be defined

        """

        try:
            val = self.config.getfloat(section, name)
        except NO_SECTION_ERROR:
            self.config.add_section(section)
            self.config.set(section, name, str(default))
            val = default
        except NO_OPTION_ERROR:
            self.config.set(section, name, str(default))
            val = default
        return val

    def getboolean(self, section, name, default=None):
        """Get a configured boolean value for a variable

        Parameters:

        *section*
            The section under which the variable is defined
        *name*
            The name of the variable
        *default*
            The value to use should the variable not be defined

        """

        try:
            val = self.config.getboolean(section, name)
        except NO_SECTION_ERROR:
            self.config.add_section(section)
            self.config.set(section, name, str(default))
            val = default
        except NO_OPTION_ERROR:
            self.config.set(section, name, str(default))
            val = default
        return val

    def set(self, section, name, value):
        """Set the value for a given variable

        *section*
            The section under which the variable is defined
        *name*
            The name of the variable
        *value*
            The value to set

        """

        val = self.config.set(section, name, str(value))
        return val
        
    def items(self, section):
        """Get a list of (name,value) pairs for all items in a section

        Parameters:

        *section*
            The section from which to retrieve (name,value) pairs

        """

        val = self.config.items(section)
        return val

    def has_section(self, secname):
        """See if the given section name is defined"""
        return self.config.has_section(secname)

    def write(self, filename='experiment.cfg'):
        """Write a file containing the values stored in the Config object.
        This file is written to the configured data directory.

        Parameters:

        *filename*
            The name of the file to create (default: experiment.cfg)

        """

        data_dir = self.get(self.experiment.config_section, 'data_dir', 'data')
        data_file = os.path.join(data_dir, filename)

        with open(data_file, 'wb') as configfile:
            info = "# SEEDS %s Experiment Configuration\n# Generated: %s\n# UUID: %s\n\n" % (S.__version__, datetime.datetime.now().strftime("%Y-%m-%d (%H:%M:%S)"), self.experiment.uuid)
            configfile.write(info)
            self.config.write(configfile)

