# -*- coding: utf-8 -*-
""" NormalResource ResourceCell represents resources that have some initial
level, which increases and decreases through inflow and decay, respectively.
Additionally, resources can flow between neighboring nodes through diffusion.
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"

from operator import attrgetter

from seeds.Action import *
from seeds.ResourceCell import *
from seeds.SEEDSError import *
from seeds.utils.parsing import parse_int_rangelist


class NormalResource(ResourceCell):
    """Environmental Resource class

    Properties:

    id
        A unique ID for this node in the resource graph
    experiment
        A reference to the Experiment being performed
    resource
        A reference to the Resource of which this object is a part
    level
        The current level of the resource
    config_section
        The name of the section where parameters for this object are defined
    inflow
        Amount of resource (in units) that flows into the environment per epoch
        (default: 0.0)
    decay
        Fraction of the resource that is removed from the environment per epoch
        (default: 0.0)
    diffusion
        Fraction of resource difference (in percent) that flows into
        neighboring resource cells per epoch.  When a node is updated, the
        levels of its neighbors are checked.  The node then distributes some of
        its resource to the neighboring nodes with lower levels of resource,
        with the neighbor with the lowest level having first priority.  The
            difference between the levels of the two nodes is computed.  This
            is the maximum amount of resource that can flow to the neighboring
            cell.  Diffusion is the percentage of this difference that is
            transferred.  At 0, no resource is transferred, while at 1, the
            entire difference (or as much as the node with higher resource has)
            between the two is transferred.  This would result in the
            neighboring node having a greater level than the focal node.  This
            value can be seen to loosely represent viscosity. (default: 0.5)
    initial
        The amount of resource (in units) present in the environment at the
        beginning (default: 0.0)

    NormalResource Resources can be defined in config files using a
    [Resource:<uniquename>] section and using the NormalResource type.  For
    example:

        [Resource:glucose]
        type = NormalResource
        topology = CartesianTopology
        initial = 0
        inflow = 0.24
        diffusion = 0.1
        decay = 0.1

    The effects of diffusion will depend on the topology, specifically the number
    of neighboring resource cells.

    """

    def __init__(self, experiment, resource, config_section, id):
        """ Initialize a NormalResource object

        Parameters:

        *experiment*
            A pointer to the Experiment
        *resource*
            A pointer to the Resource of which this is a part
        *config_section*
            The name under which the configuration parameters are specified for
            this Resource
        *id*
            A unique ID for this node in the resource graph

        """
        super(NormalResource, self).__init__(experiment=experiment,
                                             resource=resource,
                                             config_section=config_section,
                                             id=id)

        self.inflow = self.experiment.config.getfloat(self.config_section, "inflow", default=0.0)
        self.diffusion = self.experiment.config.getfloat(self.config_section, "diffusion", default=0.5)
        self.decay = self.experiment.config.getfloat(self.config_section, "decay", default=0.0)
        self.initial = self.experiment.config.getfloat(self.config_section, "initial", default=0.0)

        self.level = self.initial * 1.0

        if self.inflow < 0:
            raise ConfigurationError("NormalResource: inflow for '%s' can not be negative" % (self.resource.name))
        elif self.diffusion < 0:
            raise ConfigurationError("NormalResource: diffusion for '%s' can not be negative" % (self.resource.name))
        elif self.diffusion > 1:
            raise ConfigurationError("NormalResource: diffusion for '%s' can not be greater than 1" % (self.resource.name))
        elif self.decay < 0:
            raise ConfigurationError("NormalResource: decay for '%s' can not be negative" % (self.resource.name))
        elif self.decay > 1:
            raise ConfigurationError("NormalResource: decay for '%s' can not be greater than 1" % (self.resource.name))

    def __str__(self):
        """Produce a string to be used when a NormalResource object is printed"""
        return "NormalResource [Name: %s][Level: %f][Inflow: %f][Diffusion: %f][Decay: %f]" % (self.name, self.level, self.inflow, self.diffusion, self.decay)

    def set_inflow(self, value):
        """Set the inflow amount of the resource

        Parameters:

        *value*
            The new inflow amount of the resoruce

        """
        self.inflow = value

    def set_diffusion(self, value):
        """Set the diffusion rate of the resource

        Parameters:

        *value*
            The new diffusion rate of the resoruce

        """
        self.diffusion = value

    def set_decay(self, value):
        """Set the decay rate of the resource

        Parameters:

        *value*
            The new decay rate of the resoruce

        """
        self.decay = value

    def set_initial(self, value):
        """Set the initial level of the resource

        Parameters:

        *value*
            The new initial level of the resoruce

        """
        self.initial = value

    def update(self):
        """Update the level of the resource.  Even if the resource is
        unavailable, the resource level will be updated.
        
        """

        # Adjust the level based on inflow and decay
        newlevel = (self.level * (1 - self.decay)) + self.inflow
        self.level = max(0, newlevel)

        # Find the neighbors with lower levels
        low_neighbors = []
        for n in self.neighbors:
            if n.level < self.level:
                low_neighbors.append(n)
        #low_neighbors.sort(key=lambda l: l.level)
        low_neighbors.sort(key=attrgetter('level'))

        # Go through the neighboring nodes and transfer some resource to those
        # nodes as long as level is still above them.  Priority is given to
        # nodes with the lowest level.
        for n in low_neighbors:
            if self.level > n.level:
                xfer = min(self.level, self.level - n.level) * self.diffusion
                n.level += xfer
                self.level -= xfer

        self.level = max(0, newlevel)
        self.experiment.data['resources'][self.resource.name]['levels'][self.id] = self.level


class SetNormalResourceProperties(Action):
    """ Action to set the properties (inflow, decay, diffusion, or level) of a
    NormalResource resource

    Configuration is done in the [SetNormalResourceProperties] section

    Configuration Options:

    epoch_start
        The epoch at which to start executing (default: 0)
    epoch_end
        The epoch at which to stop executing (default: end of experiment)
    frequency
        The frequency (epochs) at which to execute (default: 1)
    priority
        The priority of this action.  Actions with higher priority get run
        first.  (default: 0)
    resource
        The name of the resource whose availability to set
    cells
        A list of the ResourceCell cells whose inflow to set.  If none are
        specified, the inflows all cells will be set.
    inflow
        The inflow value to be used.  If not specified, inflow will not be
        altered.
    decay
        The decay value to be used.  If not specified, decay will not be
        altered.
    diffusion
        The diffusion value to be used.  If not specified, diffusion will not
        be altered.
    level
        The level value to be used.  If not specified, level will not
        be altered.


    Configuration Example:

    [SetNormalResourceProperties]
    resource = glucose
    inflow = 10.2
    epoch_start = 0
    epoch_end = 100
    frequency = 1
    priority = 0

    """

    def __init__(self, experiment, label=None):
        """Initialize the SetNormalResourceProperties Action"""

        super(SetNormalResourceProperties, self).__init__(experiment,
                                                name="SetNormalResourceProperties",
                                                label=label)

        self.threshold = self.experiment.config.getint(self.config_section, 'threshold', 0)
        self.epoch_start = self.experiment.config.getint(self.config_section, 'epoch_start', 0)
        self.epoch_end = self.experiment.config.getint(self.config_section, 'epoch_end',
                                                  default=self.experiment.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.experiment.config.getint(self.config_section, 'frequency', 1)
        self.priority = self.experiment.config.getint(self.config_section, 'priority', 0)

        self.resource = self.experiment.config.get(self.config_section, 'resource')

        try:
            self.res = self.experiment.resources[self.resource]
        except KeyError:
            raise ConfigurationError("SetNormalResourceProperties: Resource '%s' is undefined" % (self.resource))

        if self.res.type != 'NormalResource':
            raise ConfigurationError("SetNormalResourceProperties: Resource '%s' is not a NormalResource" % (self.resource))
            

        self.inflow = self.experiment.config.getfloat(self.config_section, 'inflow')
        if self.inflow and self.inflow < 0:
            raise ConfigurationError("SetNormalResourceProperties: Invalid value for inflow '%f'.  Must be nonnegative." % (self.inflow))


        self.decay = self.experiment.config.getfloat(self.config_section, 'decay')
        if self.decay and self.decay < 0:
            raise ConfigurationError("SetNormalResourceProperties: Invalid value for decay '%f'.  Must be nonnegative." % (self.decay))
        elif self.decay and self.decay > 1:
            raise ConfigurationError("SetNormalResourceProperties: Invalid value for decay '%f'.  Must not be greater than 1." % (self.decay))

        self.diffusion = self.experiment.config.getfloat(self.config_section, 'diffusion')
        if self.diffusion and self.diffusion < 0:
            raise ConfigurationError("SetNormalResourceProperties: Invalid value for diffusion '%f'.  Must be nonnegative." % (self.diffusion))
        elif self.diffusion and self.diffusion > 1:
            raise ConfigurationError("SetNormalResourceProperties: Invalid value for diffusion '%f'.  Must not be greater than 1." % (self.diffusion))

        self.level = self.experiment.config.getfloat(self.config_section, 'level')
        if self.level and self.level < 0:
            raise ConfigurationError("SetNormalResourceProperties: Invalid value for level '%f'.  Must be nonnegative." % (self.level))

        if not self.inflow and not self.decay and not self.diffusion and not self.level:
            raise ConfigurationError("SetNormalResourceProperties: Must specify value for inflow, decay, diffusion, or level")

        self.cells_str = self.experiment.config.get(self.config_section, 'cells')

        if not self.cells_str:
            self.cells = self.res.topology.graph.nodes()
        else:
            self.cells = parse_int_rangelist(self.cells_str, sorted=True)
            nids = self.res.topology.graph.nodes()
            for c in self.cells:
                if c not in nids:
                    raise ConfigurationError("SetNormalResourceProperties: Cell %d does not exist in Resource '%s'" % (c, self.resource))

    def update(self):
        """Execute the Action"""
        if self.skip_update():
	        return

        for c in self.cells:
            if self.inflow:
                self.res.topology.graph.node[c]['resource'].inflow = self.inflow
            if self.diffusion:
                self.res.topology.graph.node[c]['resource'].diffusion = self.diffusion
            if self.decay:
                self.res.topology.graph.node[c]['resource'].decay = self.decay
            if self.level:
                self.res.topology.graph.node[c]['resource'].level = self.level
