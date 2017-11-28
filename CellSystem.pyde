#! /usr/bin/env pyprocessing

from cellsystem.psystem import PSystem
system = PSystem( gridDimensions=(100, 100) )

def setup():
	# Prepare window
    size(700, 700)
    frameRate(10)
    
    # Initialize the system
    system.seed()
    
    # Display
    background(200)
    system.draw()
# ---
    
def draw():
	# Prepare canvas
    background(200)
    fill(0)
    text("Framerate : %d" % frameRate, 10, 10)
    
    # How many cells are there?
    total = system.totalCells()
    alive = system.totalAliveCells()
    text("Total cells : %d, Alive: %d" % (total, alive), 
         10, 30) 
    
    # Draw next step
    system.step( singleCell=False )
    system.draw()
# ---
    
