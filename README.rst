==============================================================
SEEDS - Stochastic Ecological and Evolutionary Dynamics System
==============================================================

:Created by:
    Brian Connelly <bdc@msu.edu> and Luis Zaman <zamanlui@msu.edu>
:Website:
    https://github.com/briandconnelly/seeds


Expanded Documentation:
-----------------------
The primary source for documentation is the SEEDS Wiki_.  Here, detailed
installation instructions, how-to guides, code templates, and example
experiments are provided.


Installing SEEDS:
-------------------
SEEDS requires Python version 2.6.5 or greater.  As of version 1.0.9, SEEDS
also supports Python 3.  Additionally, SEEDS requires the NetworkX_ package.

Installation is done using the standard Python Distribution Utilities and can
be as straightforward as running "python setup.py install".  For further
instructions on this process, please see the SEEDS Wiki_ or the official
Distutils documentation at http://docs.python.org/install/index.html.


Running SEEDS:
--------------
Out of the box, SEEDS includes simple experiments in the examples directory.
These experiments can be run once SEEDS has been installed on your system.
See the README.txt file in a specific directory to learn about the experiment,
how to configure it, and how to perform it.


Expanding SEEDS:
----------------
SEEDS is designed as a plugin-based framework.  This means that you can
create and use your own cell types, topologies, and actions and use these
immediately without modifying the base SEEDS framework.

To create experiments that model behaviors of interest to you, a Cell type will
need to be created.  Additionally, sample Cell types can be found in the
examples directory, and a template can be found in the templates directory.

For further information abou plugins, please see the SEEDS Wiki_.


Reporting Bugs and Feature Requests:
------------------------------------
SEEDS is under constant development.  To see which features and changes are
planned or to report bugs, visit http://github.com/briandconnelly/seeds/issues.


License:
--------
Seeds is released under the `Apache License, Version 2.0`__.  For more
information, see the files LICENSE.txt_ and NOTICE.txt_.


.. _Wiki: https://github.com/briandconnelly/seeds/wiki
.. _NetworkX: http://networkx.lanl.gov/
.. _Apache: http://www.apache.org/licenses/LICENSE-2.0
__ Apache_
.. _LICENSE.txt: https://github.com/briandconnelly/seeds/blob/master/LICENSE.txt
.. _NOTICE.txt: https://github.com/briandconnelly/seeds/blob/master/NOTICE.txt
