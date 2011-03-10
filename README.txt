Lettuce Stochastic Cellular Artificial Life Simulator

Created by: Brian Connelly <bdc@msu.edu>, Luis Zaman <zamanlui@msu.edu>
Website: http://www.cse.msu.edu/~connel42/lettuce/
Repository: git@github.com:briandconnelly/lettuce.git


INSTALLING LETTUCE:
-------------------------------------------------------------------------------

Lettuce requires the NetworkX package, available at http://networkx.lanl.gov/.
Additionally, Lettuce requires Python version 2.6.5 or greater.

TODO: setup script.

If you specified the directory into which Lettuce was installed, you wil need
to make sure it is searchable in your Python environment.  This can be done by
placing the directory into which it was installed in your PYTHONPATH.


RUNNING LETTUCE:
-------------------------------------------------------------------------------
Out of the box, Lettuce can run a simple experiment that examines the dynamics
of a population of 100,000 Rock-Paper-Scissors players.  To do this, copy the
files runlettuce.py and lettuce.cfg into a new directory.  The simulation can
then be run by typing "python runlettuce.py".  Data will be placed into a new
directory named data.

The configuration of this experiment can be changed by editing lettuce.cfg.


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

