import random as rnd
from Cell import Cell

class CellLine:
    """Handles the specimens of a specific cell lineage.
    A cell lineage is a group of cells that have a common ancestor, we represent the common \
    ancestor by it's genome, so, in this setting, the cells in a cell line share a common \
    ancestral genome.
    This structure is in charge of holding this ancestral code and managing the cells \
    creating new cells when needed and cleaning up the dead ones.
    
    
    Atributes
    ---------    
            + Ancestral genome: A string to which all cells genomes come from.
            
            + Cells: The group of cells belonging to this cell line.
            
            + System: The system this cells form a part of.
            
            + Current cell index: Each cell has a unique identification label (index). 
                                  This is the label to place in the next cell to be born
    """
    def __init__(self, system = None, genome = ""):
        self.currentIndex = 0
        self.cells = []
        self.system = system
        self.genome = genome
    # ---
        
    def addCellTo(self, site, state = None):
        """Get a new, initialized cell
        """
        # Create the new cell
        new = self.newCell()
        new.init(state = state)
        new.addTo(site)
        
        return new # Return the new cell
    # ---
        
    def newCell(self):
        """ Get a new blank cell in this lineage and system.
        """
        new = Cell(system = self.system, 
                   cellLine = self, 
                   index = self.currentIndex)
        self.cells.append( new )
        self.currentIndex += 1
        return new
    # ---
    
    def __len__(self):
        """Get the total of cells in this lineage
        """
        return len(self.cells)
    # ---
    
    def __getitem__(self, item):
        return self.cells[item]
    # ---
    
    def aliveCells(self):
        return self.cells
    # ---
    
    def pickRandomCell(self):
        return rnd.choice(self.cells)
        
        