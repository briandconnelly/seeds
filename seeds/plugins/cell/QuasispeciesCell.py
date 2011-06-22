# -*- coding: utf-8 -*-
""" 
This Cell type is an implementation of the classic quasispecies model with
two peaks, a high but narrow peak, and a lower but wider peak. We implement
this cell type as a bit string, where the first bit represents if the organism
is on the wide peak or not (0 = narrow, 1 = wide) and the remaining bits dictate
where in the fitness landscape the genotype is. The more bits set to 1, the higher
the fitness. 

These two peaks are implemented as a polynomial function, where the order of the
function determines the steepness of the peak (i.e. x^3 is less steep than x^5).
The wide peak is a linear function where fitness varies from 0, to wide_max_value
with the number of bits set to 1. 

The classic quasispecies result is that when mutation rates are low, the quasispecies 
occupies the narrow peak since it has higher fitness. However, with higher mutation
rates the average fitness of a quasispecies is lower due to genotypes "falling" off
the peak. In these high mutation rate environments, the quasispecies is expected to
occupy the lower, but wider peak.

In this implementation, all cells die at the same rate. However, cells that replace
the empty space are chosen proportional to fitness (roulette wheel selection). When 
organisms reproduce, there is a per-site probability of flipping a bit, thus mutating
the genotype. 

"""

__author__ = "Luis Zaman <zamanlui@msu.edu>"
__credits__ = "Luis Zaman, Brian Connelly"

import random

from seeds.Cell import *
from seeds.SEEDSError import *

class QuasispeciesCell(Cell):
    """
    This cell type is an implementation of a quasispecies model using
    bitstrings.  See the top-level comment block for a more detailed
    explanation, also see Martin Nowak's Evolutionary Dynamics (chapter 3) for
    a slightly more in depth review. 
    
    The following config options should be specified in a [QuasispeciesCell]
    section of the seeds.cfg file:
    
    death_rate
        death rate of cells (float, [0,1])
    genotype_length
        number of bits the genotypes use (int, [2,])
    site_mut_rate
        probability of a site mutating (applied per site) (float, [0,])
    narrow_polynomial_order
        the order of the polynomial defining the narrow peak (int, [1,])
    wide_max_value
        maximum fitness for the wide type
        
    Example - Narrow Favored:
        [QuasispeciesCell]
        death_rate = 0.2
        genotype_length = 20
        site_mut_rate = 0.005
        narrow_polynomial_order = 4
        wide_max_value = 0.75
        
    Example - Wide Favored:
        [QuasispeciesCell]
        death_rate = 0.2
        genotype_length = 20
        site_mut_rate = 0.1
        narrow_polynomial_order = 4
        wide_max_value = 0.75

    """

    types = ['Empty', 'Narrow', 'Wide']

    EMPTY = 0
    NARROW = 1
    WIDE = 2

    def __init__(self, experiment, population, id, type=-1):
        """Initialize a QuasispeciesCell object

        The type for the cell is selected at random.

        Parameters:

        *experiment*
            A reference to the Experiment
        *population*
            A reference to the Population in which the Cell exists
        *id*
            A unique ID for the cell
        *type*
            The type of cell to initialize (-1 for random)

        """

        super(QuasispeciesCell, self).__init__(experiment, population, id)

        self.death_rate = self.experiment.config.getfloat('QuasispeciesCell', 'death_rate')
        self.genotype_length = self.experiment.config.getint('QuasispeciesCell', 'genotype_length')
        self.site_mut_rate = self.experiment.config.getfloat('QuasispeciesCell', 'site_mut_rate')
        self.narrow_polynomial_order = self.experiment.config.getfloat('QuasispeciesCell', 'narrow_polynomial_order')
        self.wide_max_value = self.experiment.config.getfloat('QuasispeciesCell', 'wide_max_value')
        
        #make sure all of the parameters are okay
        if self.death_rate < 0:
            raise ConfigurationError("QuasispeciesCell: death_rate must be non-negative")
        elif self.genotype_length <= 1:
            raise ConfigurationError("QuasispeciesCell: genotype_length must be greater than 1")
        elif self.site_mut_rate < 0:
            raise ConfigurationError("QuasispeciesCell: site_mut_rate must be non-negative")
        elif self.narrow_polynomial_order <= 0:
            raise ConfigurationError("QuasispeciesCell: narrow_polynomial_order must be greater than 0")
        elif self.wide_max_value < 0:
            raise ConfigurationError("QuasispeciesCell: wide_max_valut must be at least 0")

        #generate a random genotype
        self.genotype = [random.randint(0,1) for i in xrange(self.genotype_length)]
        
        if type == -1:
            #determine type from bitstring genotype, we'll say that 0 = narrow and 1 = wide
            #that way we can just add one to get our defined types 
            self.type = random.randint(0,len(self.types)-1)
        else:
            self.type = type
            
            #don't let this bit go negative... even though it will only happen wwith empty types
            #and they don't technically have genotypes anyway
        
        #set first bit of genotype appropriately 
        self.genotype[0] = max(self.type-1,0)
        
        self.population.increment_type_count(self.type)

        self.type_colors = ['#777777','b','r']
        
    def flip_bit(self, bit):
        """Helper function to handle single bit mutations"""
        if bit == 0:
            return 1
        else:
            return 0
            
    def mutate(self, genotype):
        """Mutate genotype based on mutation rate"""
        new_genotype = []
        for bit in genotype:
            if random.random() < self.site_mut_rate:
                new_genotype.append(self.flip_bit(bit))
            else:
                new_genotype.append(bit)
        
        return new_genotype
        
      
    def get_fitness(self, genotype):
        """ Calculate fitness based on the number of bits set to 1 and the peak
        the organism is on.

        """
        
        #get % of genotype that is set to 1
        genotype_perc_one = genotype[1::].count(1)/float(len(genotype[1::]))
        
        if genotype[0] == 0:
            #raise it to the specified order to get fitness value for narrow type
            return genotype_perc_one**self.narrow_polynomial_order
        else:
            #use linear for wide type
            return genotype_perc_one*self.wide_max_value
            
            
    def choose_neighbor(self, orgs):
        """Do roulettle wheel selection between passed organisms (neighbors)
        and return winner

        """

        fitnesses = [self.get_fitness(o.genotype) for o in orgs]
        #add small amount to avoid division by 0
        sum_fitness = sum(fitnesses) + 0.0000001
        #would be faster with numpy arrays!
        norm_fitnesses = [f/float(sum_fitness) for f in fitnesses]
        
        #roll the ball, see where it falls
        r = random.random()
        partial_sum = 0
        for i in xrange(len(norm_fitnesses)):
            if partial_sum <= r <= partial_sum + norm_fitnesses[i]:
                return orgs[i]
            partial_sum += norm_fitnesses[i] 
        
        print "didn't find a neighbor... ", sum_fitness
        return orgs[-1]
        
    def __str__(self):
        """Produce a string to be used when the object is printed"""
        return 'Quasispecies Cell %d Type %d (%s)' % (self.id, self.type, self.types[self.type])

    def type(self):
        """Return the name of the type of this cell"""
        return self.types[self.type]

    def update(self):
        """ Update the cell based on its neighbors

        Empty cells will be replaced by a neighbor proportional to their fitness
        using roulette wheel selection. 
        
        """
        
        neighbors = self.get_neighbors()

        if self.type == self.EMPTY:
            parent = self.choose_neighbor(neighbors)
            self.type = parent.type
            
            #if we're not staying empty, mutate
            if self.type != self.EMPTY:
                self.genotype = self.mutate(parent.genotype)
                #and update type to reflect the new genotype
                self.type = self.genotype[0]+1
            self.population.update_type_count(self.EMPTY, self.type)
        else:
            #check if we should die
            if random.random() < self.death_rate:
                self.population.update_type_count(self.type, self.EMPTY)
                self.type = self.EMPTY
                
