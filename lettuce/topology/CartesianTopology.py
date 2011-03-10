"""
Topology in which the location of each Cell is represented by points randomly
placed on a 2D plane.  Each Cell is connected to a configured expected number
of neighbors.

This topology was originally presented and used used in the publication:

    B.D. Connelly, L. Zaman, C. Ofria, and P.K. McKinley, "Social structure and
    the maintenance of biodiversity," in Proceedings of the 12th International
    Conference on the Synthesis and Simulation of Living Systems (ALIFE), pp.
    461-468, 2010.

"""

__author__ = "Luis Zaman <zamanlui@msu.edu>"
__version__ = "0.9.0"
__credits__ = "Luis Zaman, Brian Connelly, Philip McKinley, Charles Ofria"

import random
import math

from lettuce.CellManager import *
from lettuce.topology.Topology import *


class CartesianTopology(Topology):
    """
    Topology based on points in Cartesian space on a 2D plane

    Points are placed randomly on a unit two-dimensional Cartesian plane.
    Each cell is connected to those cells that fall within a given distance.
    This distance is calculated to yield an expected number of neighbors
    equal to the expected_neighbors configuration parameter.

    Configuration: All configuration parameters are specified in a
        [CartesianTopology] block.

    size
        Total number of Cells in the topology (Integer)
    periodic_boundaries
        Whether or not to use periodic boundary conditions, which connects the
        edges of the plane, forming a torus. (Boolean)
    expected_neighbors
        The number of neighbors (expected) each cell will have.

    Example:

    [CartesianTopology]
    size = 100000
    periodic_boundaries = True
    expected_neighbors = 20

    """

    def __init__(self, world, id):
        """Initialize a CartesianTopology object

        Parameters:

        *world*
            A reference to the World
        *id*
            A unique ID assigned to the created CartesianTopology

        """

        Topology.__init__(self, world, id)
        self.size = self.world.config.getint('CartesianTopology', 'size')
        
        self.periodic_boundaries = self.world.config.getboolean('CartesianTopology', 'periodic_boundaries', default=False)
        self.cm = CellManager(self.world, self)
        self.cellCoords = []
        self.binGrid =[]
        self.expectedNeighbors = self.world.config.getint('CartesianTopology', 'expected_neighbors')
        
        if self.expectedNeighbors != -1 and self.expectedNeighbors > 1 and self.expectedNeighbors < 120:
            self.radius = math.sqrt( (self.expectedNeighbors / float(self.size - 1 )) / math.pi)
        
        self.z = int(math.ceil(1/self.radius))
        self.rsquurd = self.radius ** 2
        
        for i in xrange(self.z):
            self.binGrid.append([])
            for j in xrange(self.z):
                self.binGrid[i].append([])
                
        for i in xrange(self.size):
            self.cells.append(self.cm.newcell(i))

            #assign a cartesian coordinate to this cell
            xy = (random.random(), random.random())
            self.cellCoords.append(xy)
            self.cells[i].coords = xy
            
            #bin this cell
            binXY = self.get_bin_coords(xy)
            self.binGrid[binXY[0]][binXY[1]].append(i)
            
        self.graph.add_nodes_from(range(self.size))
        
        self.setup_graph()

    def get_neighbors(self, cell):
        """Get a list of neighbor cell IDs for the given Cell

        Parameters:

        *cell*
            The cell whose neighbors to find

        """

        return [self.cells[id] for id in self.graph.neighbors(cell.id)]

    def setup_graph(self):
        """Setup the graph, adding edges between Cells (vertices) that fall
        within a certain distance of each other
        
        """

        nulls = 0
        for x in xrange(self.z):
            for y in xrange(self.z):
                potentials = self.get_potential_neighbors((x, y))
                for point in self.binGrid[x][y]:
                    num = 0
                    for neighbor in potentials:
                        if self.calc_distance(self.get_cart_coords(point), self.get_cart_coords(neighbor)) and neighbor != point:
                            self.graph.add_edge(point, neighbor)
                            num += 1
                    if num == 0:
                        nulls += 1
                        self.graph.add_edge(point, random.choice(range(self.size)))
                
                self.binGrid[x][y] = []
                
        
    def get_bin_coords(self, cartXY):
        """Get a tuple containing the bin cell in which a given point resides"""
        x = cartXY[0]
        y = cartXY[1]
        
        grid_x = int(math.floor(x/self.radius))
        grid_y = int(math.floor(y/self.radius))

        return (grid_x, grid_y)
        
    def get_cart_coords(self, cellID):
        """Retrieve the coordinates for a given cell ID

        Parameters:

        *cellID*
            The ID of the cell whose coordinates to get
        
        """
        return (self.cellCoords[cellID])
        
    def get_potential_neighbors(self, gridXY):
        """Looking at neighboring bins, get a list of potential neighbor Cells
        
        Parameters:

        *gridXY*
            A tuple containing the coordinates of the Cell in question
        
        """

        toReturn = []
        for x in range(-1, 2):
            for y in range(-1,2):
                if self.periodic_boundaries:
                    toReturn += self.binGrid[(gridXY[0]+x)%self.z][(gridXY[1]+y)%self.z]
                else:
                    newX = gridXY[0] + x
                    newY = gridXY[1] + y
                    if newX >= 0 and newX < self.z and newY >= 0 and newY < self.z:
                        toReturn += self.binGrid[newX][newY]
        return toReturn
        
    def calc_distance(self, cart_xy1, cart_xy2):
        """Calculate the Cartesian distance between two points"""
        if self.periodic_boundaries:
            dist_x = abs(cart_xy1[0] - cart_xy2[0])
            dist_y = abs(cart_xy1[1] - cart_xy2[1])
            dist_x = min(dist_x, 1-dist_x)
            dist_y = min(dist_y, 1-dist_y)
            
            return self.rsquurd >= dist_x**2 + dist_y **2
             
        return self.rsquurd >= (cart_xy1[0] - cart_xy2[0])**2 + (cart_xy1[1] - cart_xy2[1])**2

