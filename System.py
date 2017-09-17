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
    
    def step(self):
        """ Move the state of the system one step forward in time
        """
        # Pick one random cell
        cell = self.cells.pickRandomCell()
        cell.growOlder()
        
        # Perform an action on the cell
        actions = cell.availableActions()
        action = rnd.choice(actions)
        cell.performAction(action)
    # ---
        
    def at(self, i, j):
        """Get the site at the specified coordinates
        """
        return self.grid[i][j]
    # ---
           
    def totalCells(self):
        """Returns the total number of cells in the system.
        """
        return self.cells.totalCells()
    # ---