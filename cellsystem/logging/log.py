class Log:
    "A logger class that works as a register of the actions of a cell system."
    
    def __init__(self, *args, **kwargs):
        pass
    # ---
    
    def preparefor(self, actionname, *args, **kwargs):
        'Save previous state before the entity takes the given action.'
        getattr(self, 'preparefor_'+actionname)(*args, **kwargs)
    # ---
        
    def log(self, actionname, *args, **kwargs):
        'Log the action.'
        getattr(self, 'log_'+actionname)(*args, **kwargs)
    # ---
# ---Log