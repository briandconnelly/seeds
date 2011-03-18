#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from distutils.core import setup

import lettuce as L

if os.path.exists('MANIFEST'): os.remove('MANIFEST')

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'")
    print()

if sys.version_info[:2] < (2, 6):
    print("Lettuce requires Python version 2.6 or later (%d.%d detected)." %
    sys.version_info[:2])
    sys.exit(-1)

if __name__ == "__main__":

    with open('README.txt') as file:
        ldesc = file.read()

    setup(
        name = "lettuce",
        version = L.__version__,
        packages = ['lettuce','lettuce.action','lettuce.cell','lettuce.topology'],
        license = L.__license__,
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
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Artificial Life"
        ],
        long_description = ldesc
)

