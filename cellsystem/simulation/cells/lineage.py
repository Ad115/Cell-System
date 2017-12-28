import random as rnd
from .cell import Cell
from .logging import logged


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

    def __init__(self,
                 system,
                 genome=None,
                 genomeAlphabet=None,
                 recycleDeadCells=True):
        """Creation of a cell lineage.

        Parameters:
            :param genome: (optional) A sequence representing the base
                            genome of the cells from this line.
            :param genomeAlphabet: (optional) The items of which the genome
                                   sequence is formed.

            If a custom genome is passed, the genome alphabet should be
            passed too unless it is formed of the letters in "ACGT".

            Also, dead cells are recycled by default, this helps to improve
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
            genome = 10 * 'A'
        self.genome = genome

        # Check if the genome alphabet option was set
        if not genomeAlphabet:
            genomeAlphabet = "ACGT"
        self.genomeAlphabet = genomeAlphabet

        # Validate the resulting genome/genome alphabet combination
        if not self.validateGenome(genome, genomeAlphabet):
            # ERROR
            raise ValueError(
                '"genome" must contain only letters\
                 present in the "genomeAlphabet"' )
    # ---
    
    @classmethod
    def validateGenome(cls, genome, genomeAlphabet):
        """Check if the genome is assembled from the genome alphabet."""
        # Eliminate dups
        genomeLetters = set(genome)
        # Are they valid?
        return all( (l in genomeAlphabet) for l in genomeLetters )
    # ---

    @logged('newcell', prepare=False)
    def addCellTo(self, site):
        """Add a new, initialized cell to the given site.

        Return the added cell to the caller.

        """
        new = self.newCell()
        new.addTo(site)
        # Return the new cell
        return new
    # ---

    def newCell(self):
        """Get a new blank cell in this lineage and system."""
        # Fetch a blank cell
        if self.recycleDeadCells and self.deadCells:
            # Fetch a dead cell to recycle
            new = self.cellToRecycle()
            self.recycleCell(new)
        else:
            # Fetch a fresh, new cell
            new = Cell( cellLine = self,
                        index = self.currentIndex )
            self.currentIndex += 1
            self.cells.append(new)

        # Update state to take new cell into account
        self.aliveCells.add(new)
        return new
    # ---

    def cellToRecycle(self):
        """Return a cell from the dead ones."""
        recycled = self.deadCells.pop()
        return recycled
    # ---

    def recycleCell(self, cell):
        """Clear previous information from a cell."""
        # Place new ID
        cell.index = self.currentIndex
        self.currentIndex += 1
        # Delete age
        cell.age = 0
    # ---

    def getAliveCells(self):
        """Return the cells currently alive."""
        return self.aliveCells
    # ---

    def totalAliveCells(self):
        """Return the total number of alive cells."""
        return len(self.aliveCells)
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
            n = len(self.aliveCells)
        # If n equals 1, return a single cell
        elif n == 1:
            [singleCell] = rnd.sample(self.aliveCells, 1)
            return singleCell
        # Return a sample of size n
        return rnd.sample(self.aliveCells, n)
    # ---

    def handleDeath(self, dying):
        """Process a dying cell.

        This means removing from the alive cells and adding to the dead ones,
        maybe to recicle it when another is born.

        """
        self.aliveCells.remove(dying)
        self.deadCells.add(dying)
    # ---
# --- CellLine