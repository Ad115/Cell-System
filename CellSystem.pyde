from PSystem import PSystem
system = PSystem()
t=0

def setup():
    size(800, 800)
    background(100)
    system.init( gridDimensions=(50,50) )
    system.seed()
    system.draw()
# ---
    
def draw():
    background(100)
    
    global t
    t = t+1
    text("Framerate : %d" % frameRate, 100, 100)
    text("Total cells : %d" % system.totalCells(), 100, 200) 
    
    system.step()
    system.draw()
# ---
    