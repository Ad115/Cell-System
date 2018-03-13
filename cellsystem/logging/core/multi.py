from .log import Log


class MultiLog(Log):
    'An aggregate of logs.'
    
    def __init__(self):
        self.logs = dict()
    # ---
    
    def __getitem__(self, item):
        return self.logs[item]
    # ---
    
    def __delitem__(self, item):
        del self.logs[item]
    # ---
    
    def register(self, log, name):
        'Register a named log entity.'
        
        # Overwriting is fatal
        if name in self.logs:
            raise ValueError("Log with name '{}' already registered.".format(name))
        
        self.logs[name] = log
    # ---
    
    def preparefor(self, actionname, *args, **kwargs):
        'Save previous state before the entity takes the given action.'
        
        for name,log in self.logs.items():    
            log.preparefor(actionname, *args, **kwargs)
    # ---
        
    def log(self, actionname, *args, **kwargs):
        'Log the action.'
        
        for name,log in self.logs.items():
            log.log(actionname, *args, **kwargs)
    # ---
# --- MultiLog

    
