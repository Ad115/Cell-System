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
            
            + Cells: The group cells belonging to this cell line.
            
            + Alive cells and Dead cells: The cells that are respectively currently alive or dead
            
            + System: The system this cells form a part of.
            
            + Current cell index: Each cell has a unique identification label (index). 
                                  This is the label to place in the next cell to be born
    """
    def __init__(self, system = None, genome = "", recycleDeadCells=True):
        self.recycleDeadCells = recycleDeadCells
        self.currentIndex = 0
        self.cells = []
        self.aliveCells = set()
        self.deadCells = set()
        self.system = system
        self.genome = genome
    # ---
        
    def addCellTo(self, site):
        """Get a new, initialized cell
        """
        # Create the new cell
        new = self.newCell()
        new.addTo(site)
        
        return new # Return the new cell
    # ---
        
    def newCell(self):
        """ Get a new blank cell in this lineage and system.
        """
        # Fetch a blank cell
        # Try to fetch a dead cell to recycle
        if self.recycleDeadCells and self.deadCells:
            new = self.fetchCellToRecycle(index = self.currentIndex) 
        else:
            new = Cell(system = self.system, 
                       cellLine = self, 
                       index = self.currentIndex)
            self.cells.append( new )
            
        # Update state to take new cell into account
        self.aliveCells.add( new )
        self.currentIndex += 1
        return new
    # ---
    
    def fetchCellToRecycle(self, index=None):
        recycled = self.deadCells.pop()
        recycled.setIndex(index)
        return recycled
    # ---
        
    
    def getAliveCells(self):
        return self.aliveCells
    # ---
    
    def totalCells(self):
        return len(self.cells)
    # ---
    
    def totalAliveCells(self):
        return len(self.aliveCells)
    # ---
    
    def totalDeadCells(self):
        return len(self.deadCells)
    # ---
    
    def sampleCells(self, all=False, n=1):
        # If it is asked for all cells, 
        # take a sample of the whole size
        if all==True:
            n = len(self.aliveCells)
        # If the default argument is set, return a single cell
        elif n == 1:
            return rnd.sample(self.aliveCells, n) [0]
        # Return a sample of size n
        return rnd.sample(self.aliveCells, n)    
    # ---
        
    def handleDeath(self, dying):
        """ Process the dying cell. This means removing from the alive cells\
        and adding to the dead ones, maybe to recicle it when another is born.
        """
        self.aliveCells.remove(dying)
        self.deadCells.add(dying)
        # Cell is now officially dead
    # ---