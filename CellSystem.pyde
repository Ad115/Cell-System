from PSystem import PSystem
system = PSystem()

def setup():
    size(600, 600)
    background(100)
    frameRate(10)
    system.init( gridDimensions=(40,40) )
    system.seed()
    system.draw()
# ---
    
def draw():
    background(100)
    fill(0)
    text("Framerate : %d" % frameRate, 10, 10)
    
    total = system.totalCells()
    alive = system.totalAliveCells()
    dead = system.totalDeadCells()
    text("Total cells : %d, Alive: %d, Dead: %d" % (total, alive, dead), 
         10, 30) 
    
    system.step(singleCell=True)
    system.draw()
# ---
    