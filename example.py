"""
Usage example of the cellsystem module.
"""
from cellsystem import System

# Create the world
system = System( gridDimensions=(50, 50) )

# Seed the world
system.seed()

# Let time flow
system.step(10)

# How is the system now?
system.totalCells(state='alive')
