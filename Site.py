import random as rnd

class Site:
    """A unit of space. Cells inhabitate in these spaces and interact with cells \
    in their neighborhood.
     
    Attributes
    ----------
            + System: The system it forms a part of.
            + Coordinates <List: i,j>: Coordinates in the matrix.
            + Guests: <List of cells>: The cells currently in this site. 
    """
    def __init__(self, system, i, j):
        self.system = system
        self.coordinates = [i,j]
        self.guests = []
    # ---
        
    def addGuest(self, guest):
        """Add the given cell as a new guest to this site.
        """
        self.guests.append( guest )
        guest.setSite(self)
    # ---
        
    def guestCount(self):
        """ Return the number of cells (a.k.a. guests) in this site
        """
        return len( self.guests )
    # ---
    
    def getRandomNeighbor(self):
        """ Returns a random site in the neighborhood of the current site
        """
        i,j = self.coordinates
        coords = (i+rnd.randint(-1,1), j+rnd.randint(-1,1))
        return self.system.at(coords)
    # ---
    
    def getFirstGuest(self):
        """
        """
        if len(self.guests) > 0:
            return self.guests[0]
        else:
            return None
    # ---
        
    def getLastGuest(self):
        if len(self.guests) > 0:
            return self.guests[-1]
        else:
            return None
    # ---
    
    def getCoordinates(self):
        return self.coordinates
    # ---