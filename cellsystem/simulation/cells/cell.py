from .logging import logged
import random as rnd

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

    def tryAction(self, log=None):
        """Perform the action according to it's probability."""
        # Sample according to the probability
        if rnd.random() < self.actionProbability():
            self.action(log = log)
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

    def __init__(self, cellLine, index):
        """Create a new cell.

        Parameters:
            :param cellLine: The lineage this cell belongs to.
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
    def coordinates(self):
        """Coordinates of the site that the cell inhabits."""
        return self.site.coordinates

    @coordinates.setter
    def coordinates(self, value):
        """Set site by coordinates."""
        self.site = self.system.at(*value)
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

    @logged('division')
    def divide(self, preserveFather=False):
        """Cell division.

        Get a new daughter of this cell and place it in a nearby
        neighboring site.

        """
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
            self.migrate()
            
        return self, daughter
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

    @logged('death')
    def die(self):
        """Cellular death."""
        self.site.removeGuest(self)
        self.cellLine.handleDeath(self)
        return self
    # ---

    def deathProbability(self):
        """Cellular death probability."""
        aliveCells = self.cellLine.totalAliveCells()
        if aliveCells > 1:
            return 0.6
        else:
            return 0
    # ---
    
    @logged('migration')
    def migrate(self):
        """Migrate to a neighboring cell."""
        # Get the destination site
        nextSite = self.site.randomNeighbor()
        # Migrate to the new site
        self.site.removeGuest(self)
        nextSite.addGuest(self)
        self.site = nextSite
        
        return self
    # ---

    def migrationProbability(self):
        """Migration probability for this cell."""
        return 1

    # ---
    
    @logged('mutation')
    def mutate(self):
        """Do a single site mutation.

        Note: The genome may not represent a nucleotide sequence, so these
        mutations may not represent SNPs.

        """
        # Get the genome characteristics
        # Convert alphabet to tuple to call rnd.choice with it
        alphabet = tuple(self.cellLine.genomeAlphabet)
        genomeLength = len(self.genome)
        # Assemble the mutation
        position = rnd.randint(0, 
                               genomeLength - 1)  # Pick a random position in the genome
        mutated = rnd.choice(alphabet)
        # Mutate
        self.mutations.append((position, mutated))
        
        return self
    # ---

    def mutationProbability(self):
        """Probability to mutate if selected for it."""
        return 1
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

    def step(self, log=None):
        """Select an action and perform it."""
        # Make the cell older
        self.growOlder()
        # Select an action
        action = rnd.choice(self.availableActions)
        # Perform the action according to it's respective probability
        action.tryAction(log=log)
    # ---
# --- Cell