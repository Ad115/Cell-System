"""
The cell simulation with logging.

"""

from .simulation import System, CellLine, World
from   .logging  import FullLog


class CellSystem(System):
    "A system simulating cell growth."
    
    def __init__(self, *args, **kwargs):
        """Initialization process.
        
        A cell system has the same attributes that a system has,
        with the addition of a 'world' representing the space
        that the cells inhabit and a 'log' that follows  and makes
        a record of the cells' actions.
        
        At initialization, a new cell lineage is registered.
        
        """
        super().__init__(*args, **kwargs)
        
        # Initialize world
        grid_dim = kwargs.get('grid_dimensions', None)
        self.add(World(grid_dimensions=grid_dim), 
                 name='world', 
                 procesable=False)
        # Initialize log
        self.add(FullLog(), name='log', procesable=False)
        
        # Initialize the cells
        self.add(CellLine(), name='cells')
        self['cells'].register_log(self['log'])
    # ---
    
    def seed(self):
        'Place a single cell in the middle of the world.'
        # Fetch the middle of the grid
        world = self['world']
        middle = world.at( world.rows//2, 
                           world.cols//2 )
        # Add cell
        self['cells'].add_cell_to(middle, 
                                  log=self['log'])
    # ---
# --- CellSystem