from cellsystem.psystem import PSystem
system = PSystem()

def setup():
	# Prepare window
    size(600, 600)
    frameRate(10)
    
    # Initialize the system
    system.init( gridDimensions=(40,40) )
    system.seed()
    
    # Display
    background(100)
    system.draw()
# ---
    
def draw():
	# Prepare canvas
    background(100)
    fill(0)
    text("Framerate : %d" % frameRate, 10, 10)
    
    # How many cells are there?
    total = system.totalCells()
    alive = system.totalAliveCells()
    dead = system.totalDeadCells()
    text("Total cells : %d, Alive: %d, Dead: %d" % (total, alive, dead), 
         10, 30) 
    
    # Draw next step
    system.step( singleCell=False )
    system.draw()
# ---
    