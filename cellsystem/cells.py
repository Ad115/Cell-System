import random as rnd

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
	# ---
    
# OOOO ******** *++++++ ------  .....____________..... ------ +++++ ****** OOOO #
# OOOO ******** *++++++ ------  .....____________..... ------ +++++ ****** OOOO #
# OOOO ******** *++++++ ------  .....____________..... ------ +++++ ****** OOOO #

class Cell:
    """ A single cell. It acts according to it's state, and the states of \
    nearby cells and sites.
    
    Attributes
    ----------
            + Index: A label that identifies it among others in the same lineage.
            + Father: The index (lineage label) of it's father
            + CellLine: The lineage this cell belongs to.
            + System: The system this cell forms part of.
            + Site: The place in the grid this cell inhabits in.
            + Age: The timesteps this cell has passed through
            + Mutations: The mutations in this cell relative to the cell lineage's reference
    """
    
    # --- --- --- --- --- ------ --- --- --- --- ---
    # Mini class used to represent an action that the cell could perform
    class _Action:
        def __init__(self, action, actionProbability):
            self.action = action
            self.actionProbability = actionProbability
            
        def tryAction(self):
            # Sample according to the probability
            if rnd.random() < self.actionProbability():
                self.action()
    # --- --- --- --- --- ------ --- --- --- --- ---
    
    def __init__(self, system, cellLine, index):
        self.index = index
        self.cellLine = cellLine
        self.system = system
        self.father = -1
        self.site = None
        self.age = 0
        self._genomeCache = None
        self.mutations = []
    # ---
        
    def init(self, site=None, father=None, mutations=None):
        """Initialize with grid site and father
        """
        self.setSite(site)
        self.setFather(father)
        # Default mutations
        if mutations:
            self.setMutations(mutations) # copy
    # ---
        
    def divide(self, preserveFather=False):
        """Get a new daughter of this cell and place it in a nearby neighboring site.
        """
        print("Cell {} dividing".format(self.index))
        
        # Create the daughter cell
        daughter = self.newDaughter()
        # Search for the site to place the daughter in
        site = self.site.getRandomNeighbor()
        daughter.addTo(site)
        
        # If the preserveFather flag is set, we want a
        # father cell and a daughter cell after the division,
        # else, we want both resulting cells to be daughters of the
        # father cell, so this cell will migrate, set to age 0 and 
        # migrate.
        if not preserveFather:
            self.resetAge()
            self.setFather(self.index)
            self.cellLine.recycleCell(self)
            self.migrate()
            
        print("\tNew cells: {} and {}".format(self.index, daughter.index))
    # ---
    
    def divisionProbability(self):
        """This return the probability that this cell will divide if it was selected for division
        """
        return 1
    # ---
        
    def newDaughter(self):
        """Get a new cell that has been set as daughter of this cell 
        """
        daughter = self.cellLine.newCell()
        daughter.init(father = self.index,
                      mutations = self.mutations # Copy under the hood
                      )
        return daughter
    # ---
    
    def growOlder(self):
        """ Increase the age of the current cell
        """
        self.age += 1
    # ---
        
    def addTo(self, site):
        """ Add the cell to the site `site`
        """
        self.setSite(site)
        site.addGuest(self)
    # ---
    
    def die(self):
        """Cellular death
        """
        self.flushGenomeCache()
        self.site.removeGuest(self)
        self.cellLine.handleDeath(self)
    # ---
    
    def deathProbability(self):
        """Cellular death
        """
        aliveCells = self.cellLine.totalAliveCells() 
        if aliveCells > 1:
            return 0.6
        else:
            return 0
    # ---
    
    def migrate(self):
        """Migrate to a neighboring cell
        """
        # Get the destination site
        nextSite = self.site.getRandomNeighbor()
        # Migrate to the new site
        self.site.removeGuest(self)
        nextSite.addGuest(self)
        self.setSite(nextSite)
    # ---
    
    def migrationProbability(self):
        """The migration probability for this cell
        """
        return 1
    # ---
    
    def mutate(self):
        """ Do a single site mutation. Note: The genome may not represent a
        nucleotide sequence, so these mutations may not be SNPs
        """
        print("Mutating cell no. {} (father {}):\n \
              \t Base genome: {} \n \
              \t Current genome: {} \n \
              \t Current mutations: {}".format(self.index, self.father, 
                                               self.getBaseGenome(), 
                                               self.getGenome(),
                                               self.mutations)
              )
        
        # Get the genome characteristics
        alphabet = self.cellLine.getGenomeAlphabet()
        genomeLength = self.getGenomeLength()
        # Assemble the mutation
        position = rnd.randint(0, genomeLength-1 ) # Pick a random position in the genome
        mutated = rnd.choice(alphabet)
        # Mutate
        self.mutations.append( (position, mutated) )
        self.flushGenomeCache()
        
        print("\t\t Final mutations: {}\n \
               \t Final genome: {}".format(self.mutations,
                                           self.getGenome())
              )
    # ---
    
    def mutationProbability(self):
        return 0.5
    # ---
                
    def availableActions(self):
        """Return a list with the possible actions to take for this cell
        """
        # Death action
        death = Cell._Action(self.die, 
                             self.deathProbability)
        # Division action
        division = Cell._Action(self.divide, 
                                self.divisionProbability)
        
        # Migration action
        migration = Cell._Action(self.migrate,
                                 self.migrationProbability)
        
        # Mutation action
        mutation = Cell._Action(self.mutate,
                                self.mutationProbability)
        
        return [mutation, migration, division, death]
    # ---
    
    def step(self):
        """Select an action and perform it
        """
        # Make the cell older
        self.growOlder()
        # Select an action
        action = rnd.choice( self.availableActions() )
        # Perform the action according to it's respective probability
        action.tryAction()
    # ---
        
    #..........Setter / Getter methods ...............................
    
    def setSite(self, site=None, coords=None): 
        # Site can be assigned by coordinates or by passing the site structure
        if site:
            self.site = site
        elif coords:
            self.site = self.system.at(*coords)
    # ---
        
    def setFather(self, father):
        if father != None:
            self.father = father
    # ---
    
    def getFather(self):
        return self.father
    # ---
    
    def getCoordinates(self):
        return self.site.getCoordinates()
    # ---
    
    def getAge(self):
        return self.age
    # ---
    
    def resetAge(self):
        self.age=0
    # ---
    
    def olderThan(self, age):
        return self.age > age
    
    def getIndex(self):
        return self.index
    # ---
    
    def setIndex(self, index):
        self.index = index
    # ---
    
    def getGenomeLength(self):
        return self.cellLine.getGenomeLength()
    # ---
    
    def getBaseGenome(self):
        return self.cellLine.getBaseGenome()
    # ---
    
    def getGenome(self):
        if self._genomeCache:
            return self._genomeCache
        else:
            # Get the original genome
            bases = list( self.getBaseGenome() )
            # Add mutations one by one
            for pos, mutated in self.mutations:
                bases[pos] = mutated
            # Assemble the final genome
            genome = ''.join(bases)
            self._genomeCache = genome
            return genome
    # ---
    
    def flushGenomeCache(self):
        self._genomeCache = None
    # ---
    
    def setMutations(self, mutations):
        self.mutations = mutations[:] # COPY
    