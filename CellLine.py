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
    
    def __init__(self, 
                 system, 
                 genome = None, 
                 recycleDeadCells=True, 
                 genomeAlphabet=None):
        """ A cell line is instantiated with an obligatory system, \
        to which the cell line belongs. Optionals are the genome and the \
        genome alphabet. If a custom genome is passed, the genome alphabet \
        should be passed too unless it is formed of the letters in "ACGT".
        Also, dead cells are recycled by default, this helps to improve \
        memory usage. 
        """
        self.recycleDeadCells = recycleDeadCells
        self.currentIndex = 0
        self.cells = []
        self.aliveCells = set()
        self.deadCells = set()
        self.system = system
        # Set the default genome
        if not genome:
            genome = 10*'A'
        self.genome = genome
        # Check if the genome alphabet option was set
        if not genomeAlphabet:
            genomeAlphabet = "ACGT"
        self.genomeAlphabet = genomeAlphabet
        # Validate the resulting genome/genome alphabet combination
        for letter in genome:
            if letter not in genomeAlphabet:
                raise ValueError('`genome` must contain only letters present in the `genomeAlphabet`')
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
        if self.recycleDeadCells and self.deadCells:
            # Fetch a dead cell to recycle
            new = self.fetchCellToRecycle()
            self.recycleCell(new) 
        else:
            new = Cell(system = self.system, 
                       cellLine = self, 
                       index = self.currentIndex)
            self.currentIndex += 1
            self.cells.append( new )
            
        # Update state to take new cell into account
        self.aliveCells.add( new )
        return new
    # ---
    
    def fetchCellToRecycle(self):
        recycled = self.deadCells.pop()
        return recycled
    # ---
    
    def recycleCell(self, cell):
        cell.setIndex(self.currentIndex)
        self.currentIndex += 1
        
    
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
    
    def getGenomeAlphabet(self):
        return self.genomeAlphabet
    # ---
    
    def getBaseGenome(self):
        return self.genome
    # ---
    
    def getGenomeLength(self):
        return len(self.genome)
    