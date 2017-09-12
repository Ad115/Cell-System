from System import System

class PSystem(System):
    """ System subclass intended for use with Processing. 
    It extends the raw System class with graphical methods for interactive \
    displaying of the state of the system.
    """
    
    def draw(self):
        """Display the current automaton's state on-screen
        """
        rows = self.rows
        cols = self.cols
        rowSize = width/rows
        colSize = height/cols
            
        # Set the size of the cells to draw
        r = (colSize + rowSize)/2
        ellipseMode(CENTER)
            
        # Draw the grid state
        for i in range(rows):
            for j in range(cols):
                cellsHere = self.cellCountAt(i, j)
                if cellsHere:
                    fill( 5*cellsHere % 255 )
                    ellipse(i*rowSize, j*colSize, r, r)