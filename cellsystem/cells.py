"""The biological agent related classes.

Every cell belongs to a cell lineage, which is in charge of creating new
cells, initializing them and managing the disposal of dead ones, also, it
contains the ancestral genome of all cells from it. The cell is an agent
that lives in the system and interacts with it. A cell can perform actions
like moving along the grid, mutating, dying, etc.

"""

import random as rnd


class CellLine:
    """
    Handles the specimens of a specific cell lineage.

    A cell lineage is a group of cells that have a common ancestor, we
    represent the common ancestor by it's genome, so, in this setting, the
    cells in a cell line share a common ancestral genome.
    This structure is in charge of holding this ancestral code and managing
    the cells creating new cells when needed and cleaning up the dead ones.

    Atributes:
            + Ancestral genome: A string to which all cells genomes come from.
            + Cells: The group cells belonging to this cell line.
            + Alive/Dead cells: The cells that are respectively alive or dead.
            + System: The system this cells form a part of.
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
            :param system: The world to which the cell line belongs.
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

    @property
    def genomeAlphabet(self):
        """Letters from which the genome is formed."""
        return self._genomeAlphabet
    # ---

    @genomeAlphabet.setter
    def genomeAlphabet(self, value):
        """Setter for the genomeAlphabet."""
        # Convert the given container to a set so that lookup becomes faster.
        self._genomeAlphabet = set(value)
    # ---

    @property
    def genome(self):
        """Reference genome for the cell line."""
        return self._genome
    # ---

    @genome.setter
    def genome(self, value):
        """Setter for the genome."""
        self._genome = value

    def genomeLength(self):
        """How long is your genome."""
        return len(self.genome)

    @classmethod
    def validateGenome(cls, genome, genomeAlphabet):
        """Check if the genome is assembled from the genome alphabet."""
        # Eliminate dups
        genomeLetters = set(genome)
        # Are they valid?
        isValid = ( (l in genomeAlphabet) for l in genomeLetters )
        return all(isValid)
    # ---

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
            new = self.fetchCellToRecycle()
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

    def fetchCellToRecycle(self):
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

    def sampleCells(self, all=False, n=1):
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
        # Cell is now officially dead
    # ---
# --- CellLine


class Cell:
    """
    A single cell.

    It acts according to it's state, and the states of nearby cells and sites.

    Attributes:
        + Index: A label that identifies it among others in the
                 same lineage.
        + Father: The index (lineage label) of it's father.
        + CellLine: The lineage this cell belongs to.
        + System: The system this cell forms part of.
        + Site: The place in the grid this cell inhabits in.
        + Age: The timesteps this cell has passed through.
        + Mutations: The mutations in this cell relative to the cell
                     lineage's reference

    """

    def __init__(self, cellLine, index):
        """Create a new cell.

        Parameters:
            :param cellLine: The lineage this cell should belong to.
            :param index: The ID of this cell in the lineage.

        """
        self.index = index
        self.cellLine = cellLine
        self.father = None
        self.site = None
        self.age = 0
        self.availableActions = self.initializeActions()
        self.mutations = []
    # ---

    @property
    def site(self):
        """System's grid site that the cell inhabits."""
        return self._site

    @site.setter
    def site(self, value):
        """Setter for the cell's site."""
        self._site = value
    # ---

    @property
    def coordinates(self):
        """Coordinates of the site that the cell inhabits."""
        return self.site.coordinates

    @coordinates.setter
    def coordinates(self, value):
        """Set site by coordinates."""
        self.site = self.system.at(*value)
    # ---

    @property
    def father(self):
        """ID of the cell's father."""
        return self._father

    @father.setter
    def father(self, value):
        """Setter for the cell's father."""
        if (value is not None) and (value < 0):
            raise ValueError('Father index cannot be < 0')
        self._father = value
    # ---

    @property
    def age(self):
        """Age of the cell in timesteps."""
        return self._age

    @age.setter
    def age(self, value):
        """Setter for the cell's age."""
        if value < 0:
            raise ValueError('Age cannot be < 0')
        self._age = value
    # ---

    def resetAge(self):
        """Return the cell to it's infantry."""
        self.age = 0
    # ---

    def olderThan(self, age):
        """Is this cell older than that?"""
        return self.age > age
    # ---

    @property
    def index(self):
        """Unique identifier of the current cell (in it's lineage)."""
        return self._index

    @index.setter
    def index(self, value):
        """Setter for the cell's index."""
        if value < 0:
            raise ValueError('Cell index cannot be < 0')
        self._index = value
    # ---

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
        return self.cellLine.genome
    # ---

    @property
    def genome(self):
        """Genome of the cell.

        It is assembled from the cell's ancestral genome and it's mutations.

        """
        # Get the original genome
        bases = list(self.ancestralGenome)
        # Add mutations one by one
        for pos, mutated in self.mutations:
            bases[pos] = mutated
        # Assemble the final genome
        genome = ''.join(bases)

        return genome
    # ---

    def genomeLength(self):
        """Cell's genome length."""
        return self.cellLine.genomeLength()
    # ---

    def initializeWith(self, site=None, father=None, mutations=None):
        """Initialize grid site, mutations and father."""
        if site:
            self.site = site
        if father:
            self.father = father
        if mutations:
            self.mutations = mutations  # copy
        self.age = 0
    # ---

    def divide(self, preserveFather=False):
        """Cell division.

        Get a new daughter of this cell and place it in a nearby
        neighboring site.

        """
        print("Cell no. {} dividing @ {}".format(self.index,
                                                 self.coordinates))

        # Create the daughter cell
        daughter = self.newDaughter()
        # Search for the site to place the daughter in
        site = self.site.randomNeighbor()
        daughter.addTo(site)

        # If the preserveFather flag is set, we want a
        # father cell and a daughter cell after the division,
        # else, we want both resulting cells to be daughters of the
        # father cell, so this cell will migrate, set to age 0 and
        # migrate.
        if not preserveFather:
            self.resetAge()
            self.father = self.index
            self.cellLine.recycleCell(self)
            self.migrate(log=False)

        print("\tNew cells: {} @ {} and {} @ {}".format(
            self.index,
            self.coordinates, daughter.index, daughter.coordinates))
    # ---

    def divisionProbability(self):
        """Probability that this cell will divide if selected for division."""
        return 1
    # ---

    def newDaughter(self):
        """Initialize a new daughter cell.

        Initialize with father and mutation attributes.

        """
        daughter = self.cellLine.newCell()
        daughter.initializeWith( father=self.index,
                                 mutations=self.mutations )
        return daughter
    # ---

    def growOlder(self):
        """Increase the age of the current cell."""
        self.age += 1
    # ---

    def addTo(self, site):
        """Add the cell to the site."""
        self.site = site
        site.addGuest(self)
    # ---

    def die(self):
        """Cellular death."""
        print("Cell no. {} dying @ site {} (father {})".format(
            self.index, self.coordinates, self.father))
        self.site.removeGuest(self)
        self.cellLine.handleDeath(self)
    # ---

    def deathProbability(self):
        """Cellular death probability."""
        aliveCells = self.cellLine.totalAliveCells()
        if aliveCells > 1:
            return 0.6
        else:
            return 0
    # ---

    def migrate(self, log=True):
        """Migrate to a neighboring cell."""
        if log:
            print("Cell no. {} migrating from site {} (father {})".format(
                self.index, self.coordinates, self.father))
        # Get the destination site
        nextSite = self.site.randomNeighbor()
        # Migrate to the new site
        self.site.removeGuest(self)
        nextSite.addGuest(self)
        self.site = nextSite

        if log:
            print("\t New site: {}".format(self.coordinates))
    # ---

    def migrationProbability(self):
        """Migration probability for this cell."""
        return 1

    # ---

    def mutate(self):
        """Do a single site mutation.

        Note: The genome may not represent a nucleotide sequence, so these
        mutations may not represent SNPs.

        """
        print("Mutating cell no. {} @ site {} (father {}):\n \
              \t Base genome: {} \n \
              \t Current genome: {} \n \
              \t Current mutations: {}"
              .format(self.index,
                      self.coordinates, self.father,
                      self.ancestralGenome, self.genome, self.mutations))

        # Get the genome characteristics
        # Convert alphabet to tuple to call rnd.choice with it
        alphabet = tuple(self.cellLine.genomeAlphabet)
        genomeLength = self.genomeLength()
        # Assemble the mutation
        position = rnd.randint(
            0, genomeLength - 1)  # Pick a random position in the genome
        mutated = rnd.choice(alphabet)
        # Mutate
        self.mutations.append((position, mutated))

        print("\t\t Final mutations: {}\n \
               \t Final genome: {}".format(self.mutations, self.genome))
    # ---

    def mutationProbability(self):
        """Probability to mutate if selected for it."""
        return 0.5
    # ---

    def initializeActions(self):
        """Return a list with the possible actions to take for this cell."""
        # Death action
        death = CellAction(self.die, self.deathProbability)
        # Division action
        division = CellAction(self.divide, self.divisionProbability)

        # Migration action
        migration = CellAction(self.migrate, self.migrationProbability)

        # Mutation action
        mutation = CellAction(self.mutate, self.mutationProbability)

        return [mutation, migration, division, death]
    # ---

    def step(self):
        """Select an action and perform it."""
        # Make the cell older
        self.growOlder()
        # Select an action
        action = rnd.choice(self.availableActions)
        # Perform the action according to it's respective probability
        action.tryAction()
    # ---
# --- Cell


class CellAction:
    """
    Cell action.

    Class used to represent actions that the cell could perform.

    """

    def __init__(self, action, actionProbability):
        """Initialize action object.

        It is initialized with a function that when called will make
        the cell perform the action and a function that when called will
        calculate the probability to perform the action.


        """
        self.action = action
        self.actionProbability = actionProbability

    def tryAction(self):
        """Perform the action according to it's probability."""
        # Sample according to the probability
        if rnd.random() < self.actionProbability():
            self.action()
# --- CellAction
