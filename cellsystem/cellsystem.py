"""
The cell simulation with logging.

"""

from .simulation import System, CellLine, World, CellAction
from   .logging  import logged, FullLog
import random as rnd

class SimpleCells(CellLine):
    """A cell line representing simple cells with default behaviors.
    
    A cell from this line performs:
        - Cell division,
        - Cell death,
        - Cell migration,
        - Cell genome mutation.
        
    """
    
    def __init__(self, *args, **kwargs):
        
        # Initialize normally.
        super().__init__(*args, **kwargs)
        
        # Register the default actions
        self.add_behaviors(self.init_behaviors())
    # ---
    
    def init_behaviors(self):
        """Assemble a list with behaviors for cells in this lineage."""
        # Death action
        death = CellAction(action = self.die, 
                           probability = self.deathProbability)
        
        # Division action
        division = CellAction(action = self.divide, 
                              probability = self.divisionProbability)

        # Migration action
        migration = CellAction(action = self.migrate, 
                               probability = self.migrationProbability)

        # Mutation action
        mutation = CellAction(action = self.mutate, 
                              probability = self.mutationProbability)

        return [mutation, migration, division, death]
    # ---
        
    @staticmethod
    @logged('migration')
    def migrate(cell):
        """Migrate to a neighboring cell."""
        # Get the destination site
        next_site = cell.site.random_neighbor()
        # Migrate to the new site
        cell.site.remove_guest(cell)
        next_site.add_guest(cell)
        cell.site = next_site
        
        return cell
    # ---

    @staticmethod
    def migrationProbability(cell):
        """Migration probability for this cell."""
        return 1
    # ---
    
    @staticmethod
    @logged('mutation')
    def mutate(cell):
        """Do a single site mutation."""
        
        # Get the genome characteristics
        # Convert alphabet to tuple to call rnd.choice with it
        alphabet = tuple(cell.genome_alphabet)
        genome_length = len(cell.genome)
        
        # Assemble the mutation
        position = rnd.randrange(genome_length) # Pick a random position in the genome
        mutated = rnd.choice(alphabet)
        
        # Mutate
        cell.add_mutation(position, mutated)
        
        return cell
    # ---

    @staticmethod
    def mutationProbability(cell):
        """Probability to mutate if selected for it."""
        return 1
    # ---

    @staticmethod
    @logged('death')
    def die(cell):
        """Cellular death."""
        cell.site.remove_guest(cell)
        cell.lineage.handle_death(cell)
        return cell
    # ---

    @staticmethod
    def deathProbability(cell):
        """Cellular death probability."""
        # Avoid killing all cells.
        if cell.lineage.total_cells > 1:
            return 0.6
        else:
            return 0
    # ---
    
    @staticmethod
    def _place_daughter(cell):
        "Add a new daughter of the cell in an appropriate site."
        
        # Create the daughter cell
        daughter = cell.new_daughter()
        
        # Place the daughter
        site = cell.site
        daughter.add_to(site.random_neighbor())
        
        return daughter
    # ---
    
    @staticmethod
    @logged('division')
    def divide(cell, preserve_father=False):
        """Cell division.

        Get a new daughter of this cell and place it in a nearby
        neighboring site.

        """
        # Create the daughter cell and add it to a site
        daughter = SimpleCells._place_daughter(cell)

        # If the preserveFather flag is set, we want a
        # father cell and a daughter cell after the division (like 
        # the gemation process on yeasts), else, we want both 
        # resulting cells to be daughters of the father cell.
        if not preserve_father:
            # New daughter placed on an appropriate site
            other_daughter = SimpleCells._place_daughter(cell)
            # Remove previous cell
            SimpleCells.die(cell)
            
        return daughter, other_daughter
    # ---
    
    @staticmethod
    def divisionProbability(cell):
        """Probability that this cell will divide if selected for division."""
        return 1
    # ---
    
# --- SimpleCells


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
        self.add_entity( SimpleCells(),
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
