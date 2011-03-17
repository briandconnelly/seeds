#!/usr/bin/env python

import sys
import os
from distutils.core import setup

if os.path.exists('MANIFEST'): os.remove('MANIFEST')

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'")
    print()

if sys.version_info[:2] < (2, 6):
    print("Lettuce requires Python version 2.6 or later (%d.%d detected)." %
    sys.version_info[:2])
    sys.exit(-1)

if __name__ == "__main__":
    setup(
        name = "lettuce",
        version = "1.0.0",
        packages = ['lettuce','lettuce.action','lettuce.cell','lettuce.topology'],
        license = "Apache Version 2",
        author = "Brian Connelly",
        author_email = "bdc@msu.edu",
        maintainer = "Brian Connelly",
        maintainer_email = "bdc@msu.edu",
        url = "https://github.com/briandconnelly/lettuce",
        download_url = "https://github.com/briandconnelly/lettuce",
        keywords = ["simulation","evolution","ecology"],
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Education",
            "License :: OSI Approved :: Apache Software License",
            "Topic :: Scientific/Engineering"
        ],
        long_description = """\
        Lettuce is an open-source stochastic artifical life simulator.
        Designed to be easy to use and easy to extend, Lettuce can be used to
        study ecological and evolutionary dynamics as well as any field that
        harnesses ecological or evolutionary processes.
        """
)

