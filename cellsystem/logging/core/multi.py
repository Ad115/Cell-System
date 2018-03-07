from .log import Log


class MultiLog(Log):
    'An aggregate of logs.'
    
    def __init__(self):
        self.logs = dict()
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
        for log in self.logs.values():
            log.preparefor(actionname, *args, **kwargs)
    # ---
        
    def log(self, actionname, *args, **kwargs):
        'Log the action.'
        for log in self.logs.values():
            log.log(actionname, *args, **kwargs)
    # ---
# --- MultiLog

    
