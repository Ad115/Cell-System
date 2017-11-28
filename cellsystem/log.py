import sys

class SimpleLogger:
    """A logger class that works as a register of the actions of a cell system.
    The SimpleLogger limits itself to print the action taken.
    """
    
    def __init__(self, file=sys.stdout):
        self.file = file
    # ---
    
    def add(self, action):
        
        
    
