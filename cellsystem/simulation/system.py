from .cells import CellLine
from .site import Site


def wrap(n, maxValue):
    """Auxiliary function to wrap an integer on maxValue.

    Examples:
            >>> # For positives: wrap(n, maxValue) = n % maxValue
            >>> [ wrap(i,3) for i in range(9) ]
            [0, 1, 2, 0, 1, 2, 0, 1, 2]

            >>> # For negatives, the pattern is continued in a natural way
            >>> for i in range(-5, 5+1): print(f'{i} : {wrap(i, 3)}')
            ...
            -3 : 0
            -2 : 1
            -1 : 2
            0 : 0
            1 : 1
            2 : 2

    """
    if n >= maxValue:
        n %= maxValue
    elif n < 0:
        # We must offset the integer to the positives
        n += abs(n//maxValue)*maxValue
    return n
# ---


# < -----
class CellSystem:
    """
    The global system and event dispatcher.

    Aware of cells, space (as a grid) and the passage of time (steps). It is
    the main struture of the program, being the only observable and given it
    coordinates all processes.

    A system is aware of:
            - Grid: The sites the action develops in.
            - Cells: The cells that live, die and interact in the grid.
            - Neighborhood: How many and which sites may directly influence or
                            be influenced by another.

    """

    def __init__(self, gridDimensions=(10, 10), genome=None, wrap=True):
        """Initialize the system.

        :param gridDimensions: Tuple specifying rows and columns.
        :param genome: Container specifying the allowed 'letters' for a genome.
        :param wrap: Boolean. Does the grid wraps on the edges? (toroidal)

        """
        # Set dimensions
        self.rows, self.cols = gridDimensions
        # Initialize grid
        self.wrap = wrap  # Toroidal wrapping behavior of the grid
        self.grid = tuple( Site(self, i,j)
                               for i in range(self.rows)
                                   for j in range(self.cols) )
        # Initialize cells
        self.cells = CellLine(genome = genome,
                              system = self)
        # Initialize neighborhood
        self.neighborhood = [ (-1,-1), (-1, 0), (-1, 1),
                              ( 0,-1), ( 0, 0), ( 0, 1),
                              ( 1,-1), ( 1, 0), ( 1, 1) ]
    # ---

    def seed(self, at_coords=None, log=None):
        """Seed automaton with a cell at the given coordinates.

        If explicit coordinates are not given, place a single cell in the
        middle of the grid.

        """
        if at_coords is None:
            # Seed in the middle of the grid
            at_coords = self.rows//2, self.cols//2
        # Get the site we're adding the cell to
        site = self.at(*at_coords)
        # Add a new cell
        self.cells.addCellTo(site, log=log)
    # ---

    def cellCountAt(self, i, j):
        """Return the number of cells in a given site."""
        return self.at(i,j).guestCount()
    # ---

    def step(self, steps=1, singleCell=False, log=None):
        """Move the state of the system `steps` steps forward in time."""
        for _ in range(steps):
            self.singleStep(singleCell, log=log)
    # ---

    def singleStep(self, singleCell=False, log=None):
        """Move the state of the system one step forward in time."""
        # Advance a single cell
        if singleCell:
            cell = self.cells.sample()
            cell.step(log=log)
        else:
            # Advance all cells
            for cell in self.cells.sample(all=True):
                # Perform an action on the cell
                cell.step(log=log)
    # ---

    def at(self, i, j):
        """Get the site at the specified coordinates."""
        # Wrap (toroidal coordinates)
        if self.wrap:
            i,j = self.wrapCoordinates(i,j)
        # The grid is 1D, so we must convert from 2D
        ij = self.cols*i + j
        return self.grid[ij]
    # ---

    def wrapCoordinates(self, i, j):
        """Return i,j wrapped on the grid dimensions."""
        # Wrap the coordinates
        i = wrap(i, self.rows)
        j = wrap(j, self.cols)
        return i,j

    def totalCells(self, state='alive'):
        """Return the total number of cells of with the given 'state'."""
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

    def totalAliveCells(self):
        """Return the total number of cells in the system."""
        return self.cells.totalAliveCells()
    # ---

    def getNeighborhood(self):
        """Return the relative coordinates of the available neighbors.

        Returns a container holding pairs of numbers. the prescence of an item
        (a,b) means that a site at i,j has a neighbor at (i+a, j+b).

        """
        return self.neighborhood
    # ---
