class Cell:
    """ A single cell. It performs action according to it's state, and the states of \
    nearby cells and sites.
    
    Attributes
    ----------
            + Index: A label that identifies it among others in the same lineage.
            + Father: The index (lineage label) of it's father
            + CellLine: The lineage this cell belongs to.
            + State: Is it alive or death?
            + System: The system this cell forms part of.
            + Site: The place in the grid this cell inhabits in.
    """
    
    def __init__(self, system, cellLine, index):
        self.index = index
        self.cellLine = cellLine
        self.system = system
        self.father = None
        self.site = None
        self.state = None
        self.age = 0
    # ---
        
    def init(self, site=None, state=None, father=None):
        """Initialize with grid site and state
        """
        self.setSite(site)
        self.setState(state)
        self.setFather(father)
    # ---
        
    def divide(self):
        """Get a new daughter of this cell and place it in a nearby neighboring site.
        """
        # Create the daughter cell
        daughter = self.newDaughter()
        # Search for the site to place the daughter in
        site = self.site.getRandomNeighbor()
        daughter.addTo(site)
    # ---
        
    def newDaughter(self):
        """Get a new cell that has been set as daughter of this cell 
        """
        daughter = self.cellLine.newCell()
        daughter.init(state = "alive", 
                      father = self.index)
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
    
    #..........Setter / Getter methods ...............................
    
    def setSite(self, site=None, coords=None): 
        # Site can be assigned by coordinates or by passing the site structure
        if site:
            self.site = site
        elif coords:
            self.site = self.system.at(*coords)
    # ---
        
    def setState(self, state):
        self.state = state
    # ---
        
    def setFather(self, father):
        if father:
            self.father = father
    # ---
    
    def getFather(self):
        return self.father
    # ---
    
    def isDead(self):
        return self.state == 'dead'
    # ---
    
    def getCoordinates(self):
        return self.site.getCoordinates()
    # ---
    
    def getAge(self):
        return self.age
    # ---
    
    def getIndex(self):
        return self.index
    # ---