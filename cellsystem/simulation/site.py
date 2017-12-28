import random as rnd


class Site:
    """
    A unit of space.

    Cells inhabitate in these spaces and interact with their neighborhood.

    Is aware of:
            + System: The system it forms a part of.
            + Coordinates <i,j>: Coordinates in the matrix.
            + Guests: <List of cells>: The cells currently in this site.

    """

    def __init__(self, system, i, j):
        """Assemble a site in which agents may inhabit.

        :param system: The system in which this system resides.
        :param i: Vertical position.
        :param j: Horizontal position.

        """
        self.system = system
        self._coordinates = (i, j)  # Set variable only once
        self.guests = set()
    # ---

    @property
    def coordinates(self):
        """Getter for the site's coordinates."""
        return self._coordinates
    # ---

    def addGuest(self, guest):
        """Add the given cell as a new guest to this site."""
        self.guests.add(guest)
        guest.site = self
    # ---

    def removeGuest(self, guest):
        """Remove the given cell as guest for this site.

        If the cell is not currently in this site, an error is throwed.
        
        """
        try:
            self.guests.remove(guest)
        except KeyError:
            raise KeyError(
                    'Guest with index {} is not at site ({},{})'
                    .format(guest.index, i, j))
    # ---

    def guestCount(self):
        """Return the number of guests residing in this site."""
        return len(self.guests)
    # ---

    def randomNeighbor(self):
        """Return a random site in the neighborhood of the current site."""
        # Get your actual coordinates
        i, j = self.coordinates
        # Select a neighbor
        neighborhood = self.system.getNeighborhood()
        n_i, n_j = rnd.choice(neighborhood)
        # Fetch the neighbor
        return self.system.at( i+n_i, j+n_j )
    # ---


# < ---------------------------------------------------------------------------