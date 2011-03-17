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
        packages = ['lettuce'],
        license = "Apache Version 2",
        author = "Brian Connelly",
        author_email = "bdc@msu.edu",
        maintainer = "Brian Connelly",
        maintainer_email = "bdc@msu.edu",
        url = "https://github.com/briandconnelly/lettuce",
        download_url = "TODO",
        keywords = ["simulation","evolution","ecology"],
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Education",
            "License :: OSI Approved :: Apache Software License",
            "Topic :: Scientific/Engineering"
        ],
        long_description = """\
        TODO
        """
)

