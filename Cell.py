class Cell:
    """ A single cell. It performs action according to it's state, and the states of \
    nearby cells and sites.
    
    Attributes
    ----------
            + Index: A label that identifies it among others in the same lineage.
            + State: Is it alive or death?
            + System: The system this cell forms part of.
            + Position: The site this cell inhabits.
    """
    
    def __init__(self, system = None, position = None, state = None, cellLine = None, father = 0, index = 0):
        self.index = index
        self.father = father
        self.cellLine = cellLine
        self.system = system
        self.position = position
        self.state = state
        
    def initialize(self, system = None, position = None, state = None):
        """
        """
        self.system = system
        self.setPosition(position)
        self.setState(state)
        
    def divide(self):
        """
        """
        # Create the daughter cell
        daughter = self.newDaughter()
        # Search for the site to place the daughter
        site = self.position.getRandomNeighbor()
        # Divide
        site.addGuest(daughter)
        daughter.setState("alive")
        
    def newDaughter(self):
        daughter = self.cellLine.getNewCell()
        daughter.initialize(system = self.system, state = "dividing")
        daughter.setFather(self.index)
        return daughter
    
    def setPosition(self, site):
        if site != None:
            self.position = site
        
    def setState(self, state):
        self.state = state
        
    def setFather(self, father):
        self.father = father 
    
    def getFather(self):
        return self.father