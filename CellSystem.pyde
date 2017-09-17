from PSystem import PSystem
system = PSystem()

def setup():
    size(800, 800)
    background(100)
    frameRate(10)
    system.init( gridDimensions=(50,50) )
    system.seed()
    system.draw()
# ---
    
def draw():
    background(100)
    text("Framerate : %d" % frameRate, 10, 10)
    
    total = system.totalCells()
    alive = system.totalAliveCells()
    dead = system.totalDeadCells()
    fill(0)
    text("Total cells : %d, Alive: %d, Dead: %d" % (total, alive, dead), 
         10, 30) 
    
    system.step(singleCell=True)
    system.draw()
# ---
    