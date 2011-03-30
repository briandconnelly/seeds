SEEDS - Stochastic Ecological and Evolutionary Dynamics System
==============================================================

:Created by:
    Brian Connelly <bdc@msu.edu> and Luis Zaman <zamanlui@msu.edu>
:Website:
    https://github.com/briandconnelly/seeds


Expanded Documentation:
-----------------------
The primary source for documentation is the SEEDS website.  Here, detailed
installation instructions, how-to guides, code templates, and example
experiments are provided.


Installing SEEDS:
-------------------
SEEDS requires the NetworkX package, available at http://networkx.lanl.gov/.
Additionally, SEEDS requires Python version 2.6.5 or greater.

SEEDS can be installed using the included setup.py script by running "python
setup.py install".

If you specified the directory into which SEEDS was installed, you will need to
make sure it is searchable in your Python environment.  This can be done by
placing the directory into which it was installed in your PYTHONPATH.


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
need to be created.  More information on this process can be found on the
SEEDS website.  Additionally, sample Cell types can be found in the examples
directory.

Once you have created your additional types or actions, place them in a
directory called "plugins", and edit seeds.cfg, instructing the experiment to
use them.  For cell types, change the value of the "cell" parameter in the
"Experiment" section.  For topologies, change the value of the "topology"
parameter in the "Experiment" section.  For actions, add it to the
comma-separated "actions" parameter in the "Experiment" section.  Parameters to
your plugins can be set in the seeds.cfg file in the section you define in
your code.


License:
--------
Seeds is released under the Apache License, Version 2.0.  For more
information, see the files LICENSE.txt and NOTICE.txt.

