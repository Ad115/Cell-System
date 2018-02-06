"""

Structures representing the biological entities.
"""

import random as rnd


class CellAction:
    """
    Cell action.

    Class used to represent actions that the cell could perform.

    """

    def __init__(self, action, probability):
        """Initialize action object.

        It is initialized with a function that when called will make
        the cell perform the action and a function that when called will
        calculate the probability to perform the action.


        """
        self.action = action
        self.probability = probability

    def try_action(self):
        """Perform the action according to it's probability."""
        # Sample according to the probability
        if rnd.random() < self.probability():
            return self.action()
# --- CellAction



class Cell:
    """
    A single cell.

    It acts according to it's state, and the states of nearby cells and sites.

    Attributes:
        + Index: A label that identifies it among others in the
                 same lineage.
        + Father: The index (lineage label) of it's father.
        + CellLine: The lineage this cell belongs to.

    """

    def __init__(self, lineage, index):
        """Create a new cell.

        Parameters:
            :param cell_line: The lineage this cell belongs to.
            :param index: The ID of this cell in the lineage.

        """
        self.index = index
        self.lineage = lineage
        self.father = None
        self.actions = self.init_actions()
    # ---

    def initialize(self, father=None):
        """Initialize grid site, mutations and father."""
        self.father = father
    # ---
    
    def divide(self):
        """Cell division.

        Get a new daughter of this cell and place it in a nearby
        neighboring site.

        """
        # Create the daughter cell
        daughter = self.new_daughter()

        # We want both resulting cells to be daughters of the
        # father cell.
        self.father = self.index
        self.lineage.recycle_cell(self, father=self.index)
            
        return self, daughter
    # ---

    def divisionProbability(self):
        """Probability that this cell will divide if selected for division."""
        return 1
    # ---

    def new_daughter(self):
        """Initialize a new daughter cell.

        Initialize with father and mutation attributes.

        """
        daughter = self.lineage.new_cell()
        daughter.initialize(father=self.index)
        return daughter
    # ---

    def init_actions(self):
        """Return a list with the possible actions to take for this cell."""
        # Division action
        division = CellAction(self.divide, self.divisionProbability)

        return [division]
    # ---

    def process(self):
        """Select an action and perform it."""
        # Select an action
        action = rnd.choice(self.actions)
        # Perform the action according to it's respective probability
        result = action.try_action()
        return result
    # ---
# --- Cell



class CellLine:
    """
    Handles the specimens of a specific cell lineage.

    A cell lineage is a group of cells that have a common ancestor, we
    represent the common ancestor by it's ancestral genome.
    This structure is in charge of holding this ancestral code and managing
    the cells creating new cells when needed and cleaning up the dead ones.

    Atributes:
            + Ancestral genome: A string-like object.
            + Cells: The cells inherited from this cell line.
            + Alive/Dead cells.
            + Current cell index: Each cell has a unique index. This is the
                                  index to place in the next cell to be born.

    """

    def __init__(self, *args, **kwargs):
        """Creation of a cell lineage."""
        self.current_index = 0
        self.cells = []
        self.alive_cells = set()
        self.genome = 10 * 'A'
        self.genome_alphabet = "ACGT"
    # ---

    def new_cell(self):
        "Get a new blank cell in this lineage and system."
        # Fetch a blank cell
        # Fetch a fresh, new cell
        new = Cell( lineage = self,
                    index = self.current_index )
        self.current_index += 1
        self.cells.append(new)

        # Update state to take new cell into account
        self.alive_cells.add(new)
        return new
    # ---
    
    def recycle_cell(self, cell, father):
        """Clear previous information from a cell."""
        # Place new ID
        cell.father = father
        cell.index = self.current_index
        self.current_index += 1
    # ---

    def sample(self, all=False, n=1):
        """Take a sample of alive cells.

        :param all: If True, return all alive cells, else, return a sample of
                    size n.
        :param n: The size of the sample. If 1, return the cell without a
                  container.

        """
        # If it is asked for all cells,
        # take a sample of the whole size
        if all:
            n = len(self.alive_cells)
        # Return a sample of size n
        return rnd.sample(self.alive_cells, n)
    # ---
        
    def process(self, *args):
        'Move a step forward in time.'
        for cell in self.sample(all=True):
            cell.process()
    # ---
# --- CellLine 




if __name__ == '__main__':
    
    # Create a new cell line
    cells = CellLine()
    print(f"Cell line: {cells}")
    
    # Create the first cell
    c = cells.new_cell()
    print(f"First cell: {c}, {c.index}")
    
    # Let it take an action (division)
    c, result = c.process()
    print(f"After division, cells are {c.index}(son of {c.father}), and {result.index} (son of {result.father})")
    
    # Let every cell take an action
    cells.process()
    
    # How is the system now?
    print([cell.index for cell in cells.sample(all=True)])
