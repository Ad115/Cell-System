from System import System

class PSystem(System):
    """ System subclass intended for use with Processing. 
    It extends the raw System class with graphical methods for interactive \
    displaying of the state of the system.
    """
    
    def draw(self):
        """Display the current automaton's state on-screen
        """
        rowSize = width/self.rows
        colSize = height/self.cols
            
        # Set the size of the cells to draw
        r = 0.8*(colSize + rowSize)/2
        
        # Prepare to draw
        ellipseMode(CENTER)
        frames = frameCount
            
        # Draw cell by cell
        for cell in self.cells.aliveCells():
            # Get cell data
            i,j = cell.getCoordinates()
            age = cell.getAge()
            index = cell.getIndex()
            
            i += r/10.0 * noise( 0.0005*frames + 10*index)
            j += r/10.0 * noise( 0.0005*frames + 20*index)
            fill( 255*exp(-0.2*age) )
            ellipse(i*rowSize, j*colSize, r, r)    
    # ---