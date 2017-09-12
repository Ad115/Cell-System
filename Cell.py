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
    
    def __init__(self, system=None, site=None, state=None, cellLine=None, father=0, index=0):
        self.index = index
        self.father = father
        self.cellLine = cellLine
        self.system = system
        self.site = site
        self.state = state
        
    def initialize(self, site=None, state=None):
        """Initialize with grid site and state
        """
        self.setSite(site)
        self.setState(state)
        
    def divide(self):
        """Get a new daughter of this cell and place it in a nearby neighboring site.
        """
        # Create the daughter cell
        daughter = self.newDaughter()
        # Search for the site to place the daughter
        site = self.site.getRandomNeighbor()
        # Divide
        site.addGuest(daughter)
        daughter.setState("alive")
        
    def newDaughter(self):
        """Get a new cell that has been set as daughter of this cell 
        """
        daughter = self.cellLine.getNewCell()
        daughter.initialize(state = "alive")
        daughter.setFather(self.index)
        return daughter
    
    #..........Setter / Getter methods ...............................
    
    def setSite(self, site=None, coords=None): 
        # Site can be assigned by coordinates or by passing the site structure
        if site:
            self.site = site
        elif coords:
            self.site = self.system.at(coords)
        else:
            pass
        
    def setState(self, state):
        self.state = state
        
    def setFather(self, father):
        self.father = father 
    
    def getFather(self):
        return self.father