"""
The cell simulation with logging.

"""

from .simulation import System, CellLine, World
from   .logging  import FullLog


class CellSystem(System):
    """A system simulating cell growth.
    
    A cell system is a system subclass, with 
    the automatic initialization of three main entities:
        
            1. Cells represented by a cell line.
            
            2. A 'world' representing the space that the cells 
               inhabit, and;
               
            3. A 'log' that follows and makes a record of the 
               cells' actions.

    """
    
    def __init__(self, *args, grid_dimensions=(100, 100), **kwargs):
        """Initialization process."""
        super().__init__(*args, **kwargs)
        
        # Initialize world
        self.add_entity( World(grid_dimensions=grid_dimensions), 
                         name='world', 
                         procesable=False)
        
        # Initialize log
        self.add_entity( FullLog(),
                         name='log',
                         procesable=False)
        
        # Initialize the cells
        self.add_entity( CellLine(),
                         name='cells')
        self['cells'].register_log(self['log'])
    # ---
    
    def seed(self):
        'Place a single cell in the middle of the world.'
        # Fetch the middle of the grid
        world = self['world']
        # Add cell
        self['cells'].add_cell_to( world.middle, 
                                   log=self['log'])
    # ---
# --- CellSystem
