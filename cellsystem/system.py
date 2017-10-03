from . import cells  # Import the classes related to the biological units

import random as rnd


class Site:
    """A unit of space. Cells inhabitate in these spaces and interact with \
    their neighborhood.

    Attributes
    ----------
            + System: The system it forms a part of.
            + Coordinates <List: i,j>: Coordinates in the matrix.
            + Guests: <List of cells>: The cells currently in this site.
    """
    def __init__(self, system, i, j):
        self.system = system
        self.coordinates = (i, j)
        self.guests = set()
    # ---

    def addGuest(self, guest):
        """Add the given cell as a new guest to this site.
        """
        self.guests.add(guest)
        guest.setSite(self)
    # ---

    def removeGuest(self, guest):
        """Remove the given cell as guest for this site, \
        throw error if the cell is not currently in this site.
        """
        self.guests.remove(guest)
    # ---

    def guestCount(self):
        """ Return the number of cells (a.k.a. guests) in this site
        """
        return len(self.guests)
    # ---

    def getRandomNeighbor(self):
        """ Returns a random site in the neighborhood of the current site
        """
        # Get your actual coordinates
        i, j = self.getCoordinates()
        # Select a neighbor
        neighborhood = self.system.getNeighborhood()
        n_i, n_j = rnd.choice(neighborhood)
        # Fetch the neighbor
        return self.system.at( i+n_i, j+n_j )
    # ---

    def getCoordinates(self):
        return self.coordinates
    # ---

# OOOO ******** *++++++ ------  .....__________..... ------ +++++ ****** OOOO #
# OOOO ******** *++++++ ------  .....__________..... ------ +++++ ****** OOOO #
# OOOO ******** *++++++ ------  .....__________..... ------ +++++ ****** OOOO #


class System:
    """The whole biological system, aware of cells, space (as a grid) and \
    the passage of time (steps).
    It is the main struture of the program, being the only observable and \
    given it coordinates all processes and automatas.

    Attributes
    ----------
            + Grid: The sites the action develops in.

            + Cells: The cells that live, die and interact in the grid.

            + Dimensions: The number of rows and columns of the grid.

            + Neighborhood: The relative positions of the neighbors of a \
                            grid site
    """

    # --- --- --- --- --- ------ --- --- --- --- ---
    # Auxiliary class function
    @classmethod
    def wrap(cls, n, maxValue):
        """ Auxiliary function to wrap an integer on maxValue
        """
        if n < 0:
            n += maxValue
        if n >= maxValue:
            n -= maxValue
        return n
    # --- --- --- --- --- ------ --- --- --- --- ---

    def __init__(self, gridDimensions=None, genome=None):
        self.rows = None
        self.cols = None
        self.cells = None
        self.grid = None
        self.neighborhood = None
        # Initialize if all necessary things are given
        if gridDimensions:
            self.init(gridDimensions, genome)
    # ---

    def init(self, gridDimensions=(10,10), genome=None):
        """Initialize the automata's grid and cell lineage
        """
        # Set dimensions
        self.rows, self.cols = gridDimensions
        # Initialize grid
        self.grid = [ [ Site(self, i,j) for j in range(self.cols) ] for i in range(self.rows) ]
        # Initialize cells
        self.cells = cells.CellLine(genome = genome,
                                    system = self)
        # Initialize neighborhood
        self.neighborhood = [ [-1,-1], [-1, 0], [-1, 1],
                              [ 0,-1], [ 0, 0], [ 0, 1],
                              [ 1,-1], [ 1, 0], [ 1, 1] ]
    # ---

    def seedAt(self, i, j):
        """ Seed automaton with a cell at the given position
        """
        # Get the site we're adding the cell to
        site = self.at(i,j)
        # Add a new cell
        self.cells.addCellTo(site)

        print("New cell added @ {}".format((i,j)))
    # ---

    def seed(self):
        """ Default seeding of the automata, place one cell in the middle of the grid.
        """
        self.seedAt(self.rows//2, self.cols//2)
    # ---

    def cellCountAt(self, i, j):
        """Returns the number of cells in a given site
        """
        return self.at(i,j).guestCount()
    # ---

    def step(self, steps=1, singleCell=False):
        """Move the state of the system `steps` steps forward in time
        """
        for _ in range(steps):
            self.singleStep(singleCell)
    # ---

    def singleStep(self, singleCell=False):
        """ Move the state of the system one step forward in time
        """
        # Advance a single cell
        if singleCell:
            cell = self.cells.sampleCells()
            cell.step()
        else:
            # Advance all cells
            for cell in self.cells.sampleCells(all=True):
                # Perform an action on the cell
                cell.step()
    # ---

    def at(self, i, j, wrap=True):
        """Get the site at the specified coordinates
        """
        # Wrap (toroidal coordinates)
        if wrap:
            i,j = self.wrapCoordinates(i,j)

        return self.grid[i][j]
    # ---

    def wrapCoordinates(self, i, j):
        """ Return i,j wrapped on the grid dimensions
        """
        # Wrap the coordinates
        i = System.wrap(i, self.rows)
        j = System.wrap(j, self.cols)
        return i,j

    def totalCells(self, state='alive'):
        """Returns the total number of cells of type `state` in the system.
        """
        if state == 'alive':
            # Total count of alive cells
            return self.cells.totalAliveCells()
        elif state == 'dead':
            # Total count of dead cells
            # (makes sense only if the recycle dead cells option is not set)
            return self.cells.totalDeadCells()
        elif state == 'all':
            # Total count of cells in the system
            # (this is usually for debug purposes)
            return self.cells.totalCells()
    # ---

    def totalDeadCells(self):
        """Returns the total number of cells in the system.
        """
        return self.cells.totalDeadCells()
    # ---

    def totalAliveCells(self):
        """Returns the total number of cells in the system.
        """
        return self.cells.totalAliveCells()
    # ---

    def getNeighborhood(self):
        """ Return the relative coordinates of the neighborhood of a site in the grid
        """
        return self.neighborhood
    # ---
