import random as rnd

class Site:
    """A unit of space. Cells inhabitate in these spaces and interact with \
    their neighborhood.
     
    Attributes
    ----------
            + System: The system it forms a part of.
            + Coordinates <List: i,j>: Coordinates in the matrix.
            + Guests: <List of cells>: The cells currently in this site. 
    """
    def __init__(self, system, i, j):
        self.system = system
        self.coordinates = [i,j]
        self.guests = set()
    # ---
        
    def addGuest(self, guest):
        """Add the given cell as a new guest to this site.
        """
        self.guests.add( guest )
        guest.setSite(self)
    # ---
    
    def removeGuest(self, guest):
        """Remove the given cell as guest for this site, \
        throw error if the cell is not currently in this site.  
        """
        self.guests.remove(guest)
    # ---
        
    def guestCount(self):
        """ Return the number of cells (a.k.a. guests) in this site
        """
        return len( self.guests )
    # ---
    
    def getRandomNeighbor(self):
        """ Returns a random site in the neighborhood of the current site
        """
        # Get your actual coordinates
        i, j = self.getCoordinates()
        # Select a neighbor
        neighborhood = self.system.getNeighborhood()
        n_i, n_j = rnd.choice(neighborhood)
        # Fetch the neighbor
        return self.system.at( i+n_i, j+n_j )
    # ---
    
    def getCoordinates(self):
        return self.coordinates
    # ---