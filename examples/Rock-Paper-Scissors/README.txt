This is an example Lettuce experiment that examines a population of
Rock-Paper-Scissors players.  At each update, a player plays its strategy
(e.g., Rock) against a randomly-selected neighbor.  If the neighbor plays a
strategy that defeats the cell (e.g., Paper), the cell will adopt the strategy
of the neighbor.

To perform this experiment, run the "runlettuce.py" script.  By default, a
population of 2500 organisms will compete for 1000 epochs.  Data indicating the
abundance of each strategy will be written to the data directory.

The parameters for this experiment can be changed by editing the lettuce.cfg
file.  By changing the number of players (size in the [CartesianTopology]
section) or the average neighborhood size (expected_neighbors in the
[CartesianTopology] section), different outcomes can occur.

