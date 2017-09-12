from CellLine import CellLine
from Site import Site

class System:
    """The whole biological system, aware of cells, space (as a grid) and the passage
    of time (steps).
    It is the main struture of the program, being the main observable and controller.
    It coordinates all processes and automatas.
    
    Attributes
    ----------
            + Grid: The sites the action develops in
            + Cells: The cells that live, die and interact in the grid
            + Dimensions <rows, cols>: The number of rows and columns of the grid
    """

    def __init__(self, gridDimensions=None, genome=None):
        self.rows = None
        self.cols = None
        self.cells = None
        self.grid = None
        # Initialize if all necessary things are given 
        if gridDimensions and genome:
            self.init(gridDimensions, genome)
        
    def init(self, gridDimensions=(10,10), genome=None):
        """Initialize the automata's grid and cell lineage
        """
        self.rows, self.cols = gridDimensions
        self.grid = [ [ Site(self, i,j) for j in range(self.cols) ] for i in range(self.rows) ]
        self.cells = CellLine(genome)
        
    def seedAt(self, i, j):
        """ Seed automaton with a cell at the given position
        """
        # Get the site we're add the cell to
        site = self.grid[i][j]
        
        # Create a new cell
        self.cells.addNew(site = site, system = self, state = "alive")
        
    def seed(self):
        """ Default seeding of the automata, place one cell in the middle of the grid.
        """
        self.seedAt(self.rows//2, self.cols//2)
        
    def cellCountAt(self, i, j):
        """Returns the number of cells in a given site
        """
        return self.grid[i][j].guestCount()
    
    def step(self):
        """ Move the state of the system one step forward in time
        """
        i = int( random(len(self.cells)) )
        cell = self.cells[i]
        cell.divide()
        
    def at(self, coords):
        """Get the site at the specified coordinates
        """
        return self.grid[coords[0]][coords[1]]
           
    def totalCells(self):
        """Returns the total number of cells in the system.
        """
        return len(self.cells)