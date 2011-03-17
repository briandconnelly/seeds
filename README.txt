Lettuce Stochastic Cellular Artificial Life Simulator

Created by: Brian Connelly <bdc@msu.edu> and Luis Zaman <zamanlui@msu.edu>
Website: https://github.com/briandconnelly/lettuce


EXPANDED DOCUMENTATION:
-------------------------------------------------------------------------------
The primary source for documentation is the Lettuce website.  Here, detailed
installation instructions, how-to guides, code templates, and example
experiments are provided.


INSTALLING LETTUCE:
-------------------------------------------------------------------------------
Lettuce requires the NetworkX package, available at http://networkx.lanl.gov/.
Additionally, Lettuce requires Python version 2.6.5 or greater.

Lettuce can be installed using the included setup.py script by running "python
setup.py install".

If you specified the directory into which Lettuce was installed, you wil need
to make sure it is searchable in your Python environment.  This can be done by
placing the directory into which it was installed in your PYTHONPATH.


RUNNING LETTUCE:
-------------------------------------------------------------------------------
Out of the box, Lettuce includes simple experiments in the examples directory.
These experiments can be run once Lettuce has been installed on your system.
See the README.txt file in a specific directory to learn about the experiment,
how to configure it, and how to perform it.


EXPANDING LETTUCE:
-------------------------------------------------------------------------------
Lettuce is designed as a plugin-based framework.  This means that you can
create and use your own cell types, topologies, and topologies and use these
immediately without modifying the base Lettuce framework.

To create experiments that model behaviors of interest to you, a Cell type will
need to be created.  More information on this process can be found on the
Lettuce website.  Additionally, sample Cell types can be found in the examples
directory.

Once you have created your additional types or actions, place them in a
directory called "plugins", and edit lettuce.cfg, instructing the experiment to
use them.  For cell types, change the value of the "cell" parameter in the
"Experiment" section.  For topologies, change the value of the "topology"
parameter in the "Experiment" section.  For actions, add it to the
comma-separated "actions" parameter in the "Experiment" section.  Parameters to
your plugins can be set in the lettuce.cfg file in the section you define in
your code.


LICENSE:
-------------------------------------------------------------------------------
Lettuce is released under the Apache License, Version 2.0.  For more
information, see the files LICENSE.txt and NOTICE.txt.

