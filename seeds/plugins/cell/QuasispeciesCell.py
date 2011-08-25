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

from seeds.Cell import *
import random

class QuasispeciesCell(Cell):
    """
    This cell type is an implementation of a quasispecies model using
    bitstrings.  See the top-level comment block for a more detailed
    explanation, also see Martin Nowak's Evolutionary Dynamics (chapter 3) for
    a slightly more in depth review. 
    
    The following config options should be specified in a [QuasispeciesCell]
    section of the seeds.cfg file:
    
        death_rate: death rate of cells (float, [0,1])
        genotype_length: number of bits the genotypes use (int, [2,])
        site_mut_rate: site_mut_rate: probability of a site mutating (applied per site) (float, [0,])
        narrow_polynomail_order: the order of the polynomial defining the narrow peak (int, [1,])
        wide_max_value: 
        
    Example - Narrow Favored:
        [QuasispeciesCell]
        death_rate = 0.2
        genotype_length = 20
        site_mut_rate = 0.005
        narrow_polynomail_order = 4
        wide_max_value = 0.75
        
    Example - Wide Favored:
        [QuasispeciesCell]
        death_rate = 0.2
        genotype_length = 20
        site_mut_rate = 0.1
        narrow_polynomail_order = 4
        wide_max_value = 0.75

    """

    types = ['Empty', 'Narrow', 'Wide']
    type_colors = ['#777777','b','r']
    max_types = 3

    EMPTY = 0
    NARROW = 1
    WIDE = 2

    def __init__(self, experiment, population, node, type=None, name="QuasispeciesCell", label=None):
        """Initialize a QuasispeciesCell object

        The type for the cell is selected at random.

        Parameters:

        *experiment*
            A reference to the Experiment
        *population*
            A reference to the Population in which the Cell exists
        *node*
            The ID of the node on which this Cell resides
        *type*
            The type of cell to initialize (randomly chosen if not provided)
        *name*
            The name of this Cell type
        *label*
            A unique label for configuring this Cell type

        """

        super(QuasispeciesCell, self).__init__(experiment, population, node=node, type=type, name=name, label=label)

        self.death_rate = self.experiment.config.getfloat(self.config_section, 'death_rate')
        self.genotype_length = self.experiment.config.getint(self.config_section, 'genotype_length')
        self.site_mut_rate = self.experiment.config.getfloat(self.config_section, 'site_mut_rate')
        self.narrow_polynomail_order = self.experiment.config.getfloat(self.config_section, 'narrow_polynomail_order')
        self.wide_max_value = self.experiment.config.getfloat(self.config_section, 'wide_max_value')
        
        #make sure all of the parameters are okay
        assert self.death_rate >= 0
        assert self.genotype_length > 1
        assert self.site_mut_rate >= 0
        assert self.narrow_polynomail_order > 0
        assert self.wide_max_value >= 0

        #generate a random genotype
        self.genotype = [random.randint(0,1) for i in range(self.genotype_length)]
        
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
        
        self.world.increment_type_count(self.type)
        
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
            return genotype_perc_one**self.narrow_polynomail_order
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
        for i in range(len(norm_fitnesses)):
            if partial_sum <= r <= partial_sum + norm_fitnesses[i]:
                return orgs[i]
            partial_sum += norm_fitnesses[i] 
        
        print("didn't find a neighbor... ", sum_fitness)
        return orgs[-1]
        
    def __str__(self):
        """Produce a string to be used when the object is printed"""
        return "Quasispecies Cell %d Type %d (%s)" % (self.id, self.type, self.types[self.type])

    def type(self):
        """Return the name of the type of this cell"""
        return self.types[self.type]

    def update(self):
        """ Update the cell based on its neighbors

        Empty cells will be replaced by a neighbor proportional to their fitness
        using roulette wheel selection. 
        
        """

        if self.type == self.EMPTY:
            parent = self.choose_neighbor(self.neighbors)
            self.type = parent.type
            
            #if we're not staying empty, mutate
            if self.type != self.EMPTY:
                self.genotype = self.mutate(parent.genotype)
                #and update type to reflect the new genotype
                self.type = self.genotype[0]+1
            self.world.update_type_count(self.EMPTY, self.type)
        else:
            #check if we should die
            if random.random() < self.death_rate:
                self.world.update_type_count(self.type, self.EMPTY)
                self.type = self.EMPTY
                
