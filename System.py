import random as rnd
from CellLine import CellLine
from Site import Site

class System:
    """The whole biological system, aware of cells, space (as a grid) and the passage \
    of time (steps).
    It is the main struture of the program, being the only observable and given it \
    coordinates all processes and automatas.
    
    Attributes
    ----------
            + Grid: The sites the action develops in
            + Cells: The cells that live, die and interact in the grid
            + Dimensions <rows, cols>: The number of rows and columns of the grid
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
        # Initialize if all necessary things are given 
        if gridDimensions:
            self.init(gridDimensions, genome)
    # ---
        
    def init(self, gridDimensions=(10,10), genome=None):
        """Initialize the automata's grid and cell lineage
        """
        self.rows, self.cols = gridDimensions
        self.grid = [ [ Site(self, i,j) for j in range(self.cols) ] for i in range(self.rows) ]
        self.cells = CellLine(genome = genome, 
                              system = self)
    # ---
        
    def seedAt(self, i, j):
        """ Seed automaton with a cell at the given position
        """
        # Get the site we're adding the cell to
        site = self.at(i,j)
        # Add a new cell
        self.cells.addCellTo(site)
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
    
    def step(self, singleCell=False):
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
           
    def totalCells(self):
        """Returns the total number of cells in the system.
        """
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
    
    