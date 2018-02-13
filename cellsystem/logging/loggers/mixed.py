from ..log import Log
from .treelogs import MutationsLog, AncestryLog
from .simple import SimpleLog

class MultiLog(Log):
    'An aggregate of logs.'
    
    def __init__(self):
        self.logs = dict()
    # ---
    
    def register(self, log, name):
        'Register a named log entity.'
        
        # Overwriting is fatal
        if name in self.logs:
            raise ValueError(f"Log with name '{name}' already registered.")
        
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

    
class FullLog(MultiLog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Register the relevant logs
        self.register(MutationsLog(), name='mutations')
        self.register(AncestryLog(), name='ancestry')
        self.register(SimpleLog(), name='simple')
    # ---
    
    def mutations(self, prune_death=False):        
        return self.logs['mutations'].fetch_tree(prune_death)
    # ---
    
    def ancestry(self, prune_death=False):
        return self.logs['ancestry'].fetch_tree(prune_death)
    # ---
