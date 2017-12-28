from ..log import Log
from .ancestry import AncestryLog
from .mutations import MutationsLog
from .simple import SimpleLog

class MALog(Log):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mutations = MutationsLog()
        self.ancestry = AncestryLog()
        
    def preparefor(self, actionname, *args, **kwargs):
        'Save previous state before the entity takes the given action.'
        self.mutations.preparefor(actionname, *args, **kwargs)
        self.ancestry.preparefor(actionname, *args, **kwargs)
    # ---
        
    def log(self, actionname, *args, **kwargs):
        'Log the action.'
        self.mutations.log(actionname, *args, **kwargs)
        self.ancestry.log(actionname, *args, **kwargs)
    # ---

    
class FullLog(Log):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mutationslog = MutationsLog()
        self.ancestrylog = AncestryLog()
        self.simplelog = SimpleLog()
        
    def preparefor(self, actionname, *args, **kwargs):
        'Save previous state before the entity takes the given action.'
        self.mutationslog.preparefor(actionname, *args, **kwargs)
        self.ancestrylog.preparefor(actionname, *args, **kwargs)
        self.simplelog.preparefor(actionname, *args, **kwargs)
    # ---
        
    def log(self, actionname, *args, **kwargs):
        'Log the action.'
        self.mutationslog.log(actionname, *args, **kwargs)
        self.ancestrylog.log(actionname, *args, **kwargs)
        self.simplelog.log(actionname, *args, **kwargs)
    # ---
    
    def ancestry(self, prune_death=False):
        t = self.ancestrylog.ancestry
        
        if prune_death:
            alive_nodes = {k for k in self.ancestrylog.alive.keys()}
            return self.prune_death(t, alive_nodes)
        
        return t
    
    def mutations(self, prune_death=False):
        t = self.mutationslog.mutations
        
        if prune_death:
            alive_nodes = {v.name for v in self.mutationslog.alive.values()}
            return self.prune_death(t, alive_nodes)
        
        return t
    
    @staticmethod
    def prune_death(tree, alive_nodes):
        # Prunning tree to represent only alive cells 
        t = tree.copy()
        ancestors = set([t])
        for node in t.traverse():
            if node.name in alive_nodes:
                ancestors |= set(node.get_descendants())
                ancestors.add(node)
        t.prune(ancestors)
        return t