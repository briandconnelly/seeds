"""
TODO
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__version__ = "0.9.0"
__credits__ = "Brian Connelly, Luis Zaman"

from lettuce.cell.Cell import *
import random

#-------------------------------------------------------------------------------

class GECCO2011Cell(Cell):
    """
    This is a Cell type used in work for GECCO2011

    This Cell type has 5 states:
        EMPTY: no organism is in the cell
        UNINFECTEDS: Uninfected host, susceptible to infection by parasite
        UNINFECTEDR: Uninfected host, resistant to infection by parasite
        INFECTEDS: Infected host, sensitive to antibiotic
        INFECTEDR: Infected host, insensitive to antibiotic

    Parasites are the only way that antibiotic resistance is provided, so
    uninfected hosts are susceptible to being killed by antibiotic.

    Uninfected hosts that are susceptible may become infected by a parasite.

    Parasites in infected hosts may die, leaving the host uninfected and
    susceptible.

    Configuration: All configuration options should be specified in a GECCO2011Cell
      block.

        death_hosts: death rate of hosts (float, [0,1])
        death_parasites: death rate of parasites (float, [0,1])
        parasite_virulence: amount by which the presence of a parasite increases
            the death rate of hosts (float, [0,1])
        min_virulence: the minimum value that virulence can evolve to (float, default=0)
        max_virulence: the maximum value virulence can evolve to (float)
        cost_resistance: amount by which resistance to parasites increases the death
            rate of hosts (float, [0,1])
        cost_antibiotic_resistance: amount by which resistance to antibiotic increases
            the death rate of parasites (float, [0,1])
        mutation_rate: rate at which mutated parameters are mutated (float, [0,1])
        mutation_sigma: mutations to parameters are drawn from a normal distribution
            with the parent's value as mean and this value as standard deviation
            (float, [0,1])
        vtrans_prob: probability of parasite being transmitted vertically from an
            infected parent to its offspring (float, [0,1])
        htrans_prob: probability of a parasite being transmitted to an uninfected,
            susceptible cell from a randomly-chosen neighbor cell if that neighbor
            is infected (float, [0,1]).
        ld100: level of Antibiotic at which 100% of cells are killed (float, [0,1])
        pct_neutralized: Percent of Antibiotic resource in cell that is degraded
            by an Infected-Insensitive host (float, [0,1])

    The "Antibiotic" resource is responsible for containing the amount of
    antibiotic present in the environment.

    """

    types = ['Empty', 'Uninfected-Susceptible', 'Uninfected-Resistant',
             'Infected-Sensitive', 'Infected-Insensitive']

    EMPTY = 0
    UNINFECTEDS = 1
    UNINFECTEDR = 2
    INFECTEDS = 3
    INFECTEDR = 4

    def __init__(self, world, topology, id):
        Cell.__init__(self, world, topology, id)
        self.world = world
        self.topology = topology
        self.id = id
        self.type = random.randint(0, len(self.types)-1)
        self.topology.increment_type_count(self.type)

        self.dh = self.world.config.getfloat('GECCO2011Cell', 'death_hosts')
        self.dp = self.world.config.getfloat('GECCO2011Cell', 'death_parasites')
        self.v = self.world.config.getfloat('GECCO2011Cell', 'parasite_virulence')
        self.minv = self.world.config.getfloat('GECCO2011Cell', 'min_virulence', 0.0)
        self.maxv = self.world.config.getfloat('GECCO2011Cell', 'max_virulence')
        self.cr = self.world.config.getfloat('GECCO2011Cell', 'cost_resistance')
        self.car = self.world.config.getfloat('GECCO2011Cell', 'cost_antibiotic_resistance')
        self.mu = self.world.config.getfloat('GECCO2011Cell', 'mutation_rate')
        self.sigma = self.world.config.getfloat('GECCO2011Cell', 'mutation_sigma')
        self.vtrans = self.world.config.getfloat('GECCO2011Cell', 'vtrans_prob')
        self.htrans = self.world.config.getfloat('GECCO2011Cell', 'htrans_prob')
        self.ld100 = self.world.config.getfloat('GECCO2011Cell', 'ld100')
        self.pct_neutralized = self.world.config.getfloat('GECCO2011Cell', 'pct_neutralized')

        self.v = random.uniform(self.minv, self.maxv)

    def __str__(self):
        return 'GECCO2011Cell ID: %d Type: %d (%s)' % (self.id, self.type, self.types[self.type])

    def G(self, neighbors):
        # This function returns the additional mortality imposed by antibiotic.
        # It should consider the level in the current cell as well as the level
        # in the neighboring cells in order to allow for cheaters and maintain
        # spatial relationships
        total_antibiotic = 0.0
        for neighbor in neighbors:
            total_antibiotic += neighbor.resource_manager.get_level("Antibiotic")

        mean_neighborhood_level = total_antibiotic/len(neighbors)

        return mean_neighborhood_level/float(self.ld100)

    def horiz_trans_prob(self):
        # Old way
        #val = self.htrans

        # Use a Michaelis-Menten equation to determine how virulence determines
        # the probability of horizontal gene transfer. ax/(b+x)
        #a = 1   # asymptote
        #b = self.maxv * 0.25   # 1/2 saturation
        #val = (a * self.v) / (b + self.v)

        # Or just linear.
        val = (self.v - self.minv) / (self.maxv - self.minv)

        return val

    def update(self, neighbors):
        self.resource_manager.update()

        if self.type == self.EMPTY:
            parent = random.choice(neighbors)

            if parent.type != self.EMPTY:
                self.type = parent.type

                self.dh = parent.dh
                self.dp = parent.dp
                self.cr = parent.cr
                self.car = parent.car
                self.mu = parent.mu
                self.sigma = parent.sigma
                self.type = parent.type

                if parent.type == self.INFECTEDS or parent.type == self.INFECTEDR:
                    # Vertical transmission
                    if random.random() < self.vtrans:
                        self.type = parent.type

                        # Mutate virulence
                        if random.random() < self.mu:
                            self.v = max(self.minv, min(self.maxv, random.normalvariate(parent.v, self.sigma)))
                        else:
                            self.v = parent.v

                        # Mutate in parasite resistence
                        if parent.type == self.INFECTEDS and random.random() < self.mu:
                            self.type = self.INFECTEDR

                        # Mutate out parasite resistence
                        if parent.type == self.INFECTEDR and random.random() < self.mu:
                            self.type = self.INFECTEDS

                    else:
                        self.type = self.UNINFECTEDS

                # Evolve parasite resistence
                if parent.type == self.UNINFECTEDS and random.random() < self.mu:
                    self.type = self.UNINFECTEDR

                # De-evolve parasite resistence
                if parent.type == self.UNINFECTEDR and random.random() < self.mu:
                    self.type = self.UNINFECTEDS

                self.topology.update_type_count(self.EMPTY, self.type)  

        elif self.type == self.UNINFECTEDS:
            # Death of host
            if random.random() < (self.dh + self.G(neighbors)):
                self.topology.update_type_count(self.type, self.EMPTY)
                self.type = self.EMPTY

        elif self.type == self.UNINFECTEDR:
            # Death of host
            if random.random() < (self.dh + self.cr + self.G(neighbors)):
                self.topology.update_type_count(self.type, self.EMPTY)
                self.type = self.EMPTY

        elif self.type == self.INFECTEDS:
            # Death of host
            if random.random() < (self.dh + self.v + self.G(neighbors)):
                self.topology.update_type_count(self.type, self.EMPTY)
                self.type = self.EMPTY

            # Death of parasite -> Becomes Uninfected-Susceptible
            elif random.random() < self.dp:
                self.topology.update_type_count(self.type, self.UNINFECTEDS)
                self.type = self.UNINFECTEDS

            # Horizontal transmission to neighboring uninfected cell
            elif random.random() < self.horiz_trans_prob():
                neighbor = random.choice(neighbors)

                if neighbor.type == self.UNINFECTEDS:
                    self.topology.update_type_count(neighbor.type, self.type)
                    neighbor.type = self.type

                    # Mutate virulence
                    if random.random() < self.mu:
                        neighbor.v = max(0, min(1, random.normalvariate(self.v, self.sigma)))
                    else:
                        neighbor.v = self.v

                    # Evolve antibiotic resistence during transmission
                    if random.random() < self.mu:
                        self.topology.update_type_count(neighbor.type, self.INFECTEDR)
                        neighbor.type = self.INFECTEDR

        elif self.type == self.INFECTEDR:
            antibiotic = self.resource_manager.get_resource("Antibiotic")
            antibiotic.level = antibiotic.level * (1 - self.pct_neutralized)

            # Death of host
            if random.random() < (self.dh + self.v + self.car):
                self.topology.update_type_count(self.type, self.EMPTY)
                self.type = self.EMPTY

            # Death of parasite -> Becomes Uninfected-Susceptible
            elif random.random() < self.dp:
                self.topology.update_type_count(self.type, self.UNINFECTEDS)
                self.type = self.UNINFECTEDS

            # Horizontal transmission to neighboring uninfected cell
            elif random.random() < self.horiz_trans_prob():
                neighbor = random.choice(neighbors)

                if neighbor.type == self.UNINFECTEDS:
                    self.topology.update_type_count(neighbor.type, self.type)
                    neighbor.type = self.type

                    # Mutate virulence
                    if random.random() < self.mu:
                        neighbor.v = max(0, min(1, random.normalvariate(self.v, self.sigma)))
                    else:
                        neighbor.v = self.v

                    # De-evolve antibiotic resistence
                    if random.random() < self.mu:
                        self.topology.update_type_count(neighbor.type, self.INFECTEDS)
                        neighbor.type = self.INFECTEDS

        else:
            print 'Error: Invalid cell type %d for cell %d' % (self.type, self.id)

