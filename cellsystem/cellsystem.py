"""
The cell simulation with logging.

"""

from .simulation import System, CellLine, World, Action
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
    
    def __init__(self, *args, genome_alphabet=None, **kwargs):
        
        # Initialize as usual.
        super().__init__(*args, **kwargs)
        
        # Register the default actions
        self.add_behaviors(*self._init_behaviors())
    # ---
    
    def _init_behaviors(self):
        """Initialize the behaviors for cells in this lineage."""
        death = Action(action=self.die, 
                       probability=self.death_probability)
        
        division = Action(action=self.divide, 
                          probability=self.division_probability)
        
        migration = Action(action=self.migrate, 
                           probability=self.migration_probability)
        
        mutation = Action(action=self.mutate, 
                          probability=self.mutation_probability)
        
        
        actions = [mutation, migration, division, death]
        
        # The relative weights of each action.
        # If an action has a bigger weigth than 
        # the others, it has a correspondingly
        # bigger probability to be chosen
        weights = [1] * len(actions)
        
        return actions, weights
    # ---
    
    @logged('newcell', prepare=False)
    def add_cell_to(self, site):
        """Add a new, initialized cell to the given site.

        Return the added cell to the caller.

        """
        new = self.new_cell()
        new.add_to(site)
        # Return the new cell
        return new
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
    def migration_probability(cell):
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
    def mutation_probability(cell):
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
    def death_probability(cell):
        """Cellular death probability."""
        # Avoid killing all cells.
        if cell.lineage.total_cells > 1:
            return 0.6
        else:
            return 0
    # ---
    
    @staticmethod
    def _init_daughter(cell):
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
        daughter = SimpleCells._init_daughter(cell)

        # If the preserveFather flag is set, we want a
        # father cell and a daughter cell after the division (like 
        # the gemation process on yeasts), else, we want both 
        # resulting cells to be daughters of the father cell.
        if not preserve_father:
            # New daughter placed on an appropriate site
            other_daughter = SimpleCells._init_daughter(cell)
            # Remove previous cell
            SimpleCells.die(cell)
            
        return daughter, other_daughter
    # ---
    
    @staticmethod
    def division_probability(cell):
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
    
    def __init__(self, *args, 
                       grid_shape=(100, 100), 
                       init_genome=None,
                       **kwargs):
        """Initialization process."""
        
        super().__init__(*args, **kwargs)
        
        # Initialize world
        self.add_entity( World(shape=grid_shape), 
                         name='world', 
                         procesable=False)
        
        # Initialize log
        self.add_entity( FullLog(),
                         name='log',
                         procesable=False)
        
        # Initialize the cells
        self.add_entity( SimpleCells(genome=init_genome),
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
