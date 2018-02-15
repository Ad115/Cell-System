"""

A world is the passive (or not?) stage where 
entities do their own thing :P

"""

import random as rnd


def wrap(n, maxValue):
    """Auxiliary function to wrap an integer on maxValue.

    Examples:
            >>> # For positives: wrap(n, maxValue) = n % maxValue
            >>> [ wrap(i,3) for i in range(9) ]
            [0, 1, 2, 0, 1, 2, 0, 1, 2]

            >>> # For negatives, the pattern is continued in a natural way
            >>> for i in range(-5, 5+1): print(f'{i} : {wrap(i, 3)}')
            ...
            -3 : 0
            -2 : 1
            -1 : 2
            0 : 0
            1 : 1
            2 : 2

    """
    if n >= maxValue:
        n %= maxValue
    elif n < 0:
        # We must offset the integer to the positives
        n += abs(n//maxValue)*maxValue
    return n
# ---

def toroidal_wrap(grid, coord):
    """Return the coordinates wrapped on the grid dimensions."""
    return tuple(wrap(x, dim_size) 
                    for x,dim_size 
                        in zip(coord, grid.grid_dimensions) )
# ---



class Site:
    """
    A unit of space.

    Cells inhabitate in these spaces and interact with their neighborhood.

    Is aware of:
            + World: The world it forms a part of.
            + Coordinates <i,j>: Coordinates in the matrix.
            + Guests: <List>: The guests currently inhabiting this site.

    """

    def __init__(self, world, coordinates):
        """Assemble a site in which agents may inhabit.

        :param world: The world which this forms a part of.
        :param coordinates: The coordinates in the world.

        """
        self.world = world
        self._coordinates = coordinates  # Set variable only once
        self.guests = set()
    # ---

    @property
    def coordinates(self):
        """Getter for the site's coordinates."""
        return self._coordinates
    # ---

    def add_guest(self, guest):
        """Add the given cell as a new guest to this site."""
        self.guests.add(guest)
        guest.site = self
    # ---

    def remove_guest(self, guest):
        """Remove the given cell as guest for this site.

        If the cell is not currently in this site, an error is throwed.
        
        """
        try:
            self.guests.remove(guest)
        except KeyError:
            raise KeyError('Guest with index {} is not at site ({})'
                                            .format(guest.index, self.coordinates))
    # ---

    def guest_count(self):
        """Return the number of guests residing in this site."""
        return len(self.guests)
    # ---

    def random_neighbor(self):
        """Return a random site in the neighborhood of the current site."""
        # Select a neighbor
        return self.world.random_neighbor_of(self)
    # ---
# --- Site



# < -----
class World:
    """
    The space in which cells inhabit. 

    Aware of space (as a grid) and the passage of time (steps). It is
    the main struture of the program, being the only observable and given it
    coordinates all processes.

    A system is aware of:
            - Grid: The sites the action develops in.
            - Cells: The cells that live, die and interact in the grid.
            - Neighborhood: How many and which sites may directly influence or
                            be influenced by another.

    """

    def __init__(self, grid_dimensions=None, wrap=toroidal_wrap):
        """Initialize the world.

        :param grid_dimensions: Tuple specifying rows and columns.
        :param wrap: Callable. How does the grid treats out-of-range coordinates?

        """
        # Set dimensions
        if grid_dimensions is None:
            grid_dimensions = (10, 10)
            
        self.grid_dimensions = grid_dimensions
        
        # Initialize grid
        self.wrap_function = wrap  # Toroidal wrapping behavior of the grid
        
        rows, cols = self.grid_dimensions
        self.grid = tuple( Site(self, coordinates=(i,j))
                               for i in range(rows)
                                   for j in range(cols) ) # Stored in 1D
        # Initialize neighborhood
        self.neighborhood = [ (-1,-1), (-1, 0), (-1, 1),
                              ( 0,-1), ( 0, 0), ( 0, 1),
                              ( 1,-1), ( 1, 0), ( 1, 1) ]
    # ---
    
    @property
    def middle(self):
        """Get the site at the middle of the world."""
        rows, cols = self.grid_dimensions
        return self.at( (rows//2, cols//2) )
    # ---

    def at(self, coordinates):
        """Get the site at the specified coordinates."""        
        # Wrap (toroidal coordinates)
        if self.wrap_function:
            i,j = self.wrap_function(self, coordinates)
            
        # The grid is 1D, so we must convert from 2D
        rows, cols = self.grid_dimensions
        ij = cols*i + j
        return self.grid[ij]
    # ---

    def random_neighbor_of(self, site):
        """Return the relative coordinates of the available neighbors.

        Returns a container holding pairs of numbers. the prescence of an item
        (a,b) means that a site at i,j has a neighbor at (i+a, j+b).

        """
        # Get the site coordinates
        i,j = site.coordinates
        # Select a neighbor
        n_i, n_j = rnd.choice(self.neighborhood)
        # Fetch the neighbor
        return self.at( (i+n_i, j+n_j) )
    # ---
# --- World
