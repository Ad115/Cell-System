"""

Structures representing the biological entities.
"""

from ..logging import logged
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

    def try_action(self, cell, *args, **kwargs):
        """Perform the action according to it's probability."""
        # Sample according to the probability
        if rnd.random() < self.probability(cell):
            self.action(cell, *args, **kwargs)
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
        + Site: The place in the grid this cell inhabits in.
        + Age: The timesteps this cell has passed through.
        + Mutations: The mutations in this cell relative to the cell
                     lineage's reference

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
        self.site = None
        self.actions = self.lineage.fetch_behaviors()
        self.mutations = []
    # ---

    @property
    def coordinates(self):
        """Coordinates of the site that the cell inhabits."""
        return self.site.coordinates

    @property
    def mutations(self):
        """Record of the mutations the cell has had.

        The mutations are relative to the ancestral genome.

        """
        return self._mutations

    @mutations.setter
    def mutations(self, value):
        """Setter for the cell's mutations."""
        self._mutations = list(value)  # COPY
    # ---

    @property
    def ancestralGenome(self):
        """Ancestral genome of the cell lineage."""
        return self.lineage.genome
    # ---

    @property
    def genome(self):
        """Genome of the cell.

        It is assembled from the cell's ancestral genome and it's mutations.

        """
        # Get the original genome
        bases = list(self.ancestralGenome)
        # Add mutations one by one
        for position, mutated in self.mutations:
            bases[position] = mutated
        # Assemble the final genome
        genome = ''.join(bases)

        return genome
    # ---
    
    @property
    def genome_alphabet(self):
        """Genome alphabet of the cell line.

        The set of characters a genome is composed of.
        (The genome characters may really represent genes, aminoacids, etc...)

        """
        return self.lineage.genome_alphabet
    # ---

    def initialize(self, site=None, father=None, mutations=None):
        """Initialize grid site, mutations and father."""
        if site:
            self.site = site
        if father:
            self.father = father
        if mutations:
            self.mutations = mutations  # copy
    # ---
    
    def add_mutation(self, position, mutated):
        """Add a mutation to the cell in the given position of the genome.
        
        Note: The genome may not represent a nucleotide sequence, so these
        mutations may not represent SNPs.
        """
        mutation = (position, mutated)
        self.mutations.append(mutation)
    # ---

    def new_daughter(self):
        """Initialize a new daughter cell.

        Initialize with father and mutation attributes.

        """
        daughter = self.lineage.new_cell()
        daughter.initialize( father=self.index,
                             mutations=self.mutations )
        return daughter
    # ---

    def add_to(self, site):
        """Add the cell to the site."""
        self.site = site
        site.add_guest(self)
    # ---    

    def process(self, *args, **kwargs):
        """Select an action and perform it."""
        # Select an action
        action = rnd.choice(self.actions)
        # Perform the action according to it's respective probability
        action.try_action(self, *args, **kwargs)
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

    def __init__(self,
                 genome=None,
                 genome_alphabet=None,
                 recycle_dead=True,
                 *args,
                 **kwargs):
        """Creation of a cell lineage.

        Parameters:
            :param genome: (default 'AAAAAAAAAA') Sequence representing the 
                            base genome of the cells from this line.
            :param genomeAlphabet: (default 'ACGT') The items of which the 
                                    genome sequence is formed.
            :param recycle_dead: (default True) Repurpose dead cells when needed,
                                 this helps improve memory usage.

            If a custom genome is passed, the genome alphabet should be
            passed too unless it is formed of the letters in "ACGT".
            
        """
        self.recycle_dead = recycle_dead
        self.current_index = 0
        self.cells = []
        self.behaviors = []
        self.alive_cells = set()
        self.dead_cells = set()

        # Set the default genome
        if not genome:
            genome = 10 * 'A'
        self.genome = genome

        # Check if the genome alphabet option was set
        if not genome_alphabet:
            genome_alphabet = "ACGT"
        self.genome_alphabet = genome_alphabet

        # Validate the resulting genome/genome alphabet combination
        if not self.validate_genome(genome, genome_alphabet):
            # ERROR
            raise ValueError('"genome" must contain only letters\
                             present in the "genome_alphabet"' )
    # ---
        
    @property
    def total_cells(self):
        return len(self.alive_cells)
    # ---
    
    @staticmethod
    def validate_genome(genome, alphabet):
        "Check if the genome is assembled from the given alphabet."
        # Eliminate dups
        letters = set(genome)
        # Are they valid?
        return all((l in alphabet) for l in letters)
    # ---
    
    def fetch_behaviors(self):
        "The behaviors that the cells in this lineage perform."
        return list(self.behaviors)
    # ---
    
    def add_behaviors(self, behaviors):
        "Add the behaviors defining the cells from this cell line."
        self.behaviors += behaviors
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

    def new_cell(self):
        "Get a new blank cell in this lineage and system."
        # Fetch a blank cell
        if self.recycle_dead and self.dead_cells:
            # Fetch a dead cell to recycle
            new = self.cell_to_recycle()
            self.recycle_cell(new)
        else:
            # Fetch a fresh, new cell
            new = Cell( lineage = self,
                        index = self.current_index )
            self.current_index += 1
            self.cells.append(new)

        # Update state to take new cell into account
        self.alive_cells.add(new)
        return new
    # ---

    def cell_to_recycle(self):
        """Return a cell from the dead ones."""
        recycle = self.dead_cells.pop()
        return recycle
    # ---

    def recycle_cell(self, cell):
        """Clear previous information from a cell."""
        # Place new ID
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

    def handle_death(self, dying):
        """Process a dying cell.

        This means removing from the alive cells and adding to the dead ones,
        maybe to recycle it when another is born.

        """
        self.alive_cells.remove(dying)
        self.dead_cells.add(dying)
    # ---
    
    def register_log(self, log):
        self.log = log
    # ---
        
    def process(self, *args, **kwargs):
        'Move a step forward in time.'
        for cell in self.sample(all=True):
            cell.process(log=self.log)
    # ---
# --- CellLine
