from ..log import Log
from .treelogs import MutationsLog, AncestryLog
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
    
    def mutations(self, prune_death=False):        
        return self.fetch_tree(self.mutationslog, prune_death)
    # ---
    
    def ancestry(self, prune_death=False):
        return self.fetch_tree(self.ancestrylog, prune_death)
    # ---
    
    def fetch_tree(self, log, prune_death):
        t = log.tree.copy()
        
        if prune_death:
            alive_nodes = {node.name for node in log.alive_nodes}
            t = self.prune_death(t, alive_nodes)
        
        return t
    
    @staticmethod
    def prune_death(tree, alive_nodes):
        # Prunning tree to represent only alive cells 
        ancestors = set([tree])
        for node in tree.traverse():
            if node.name in alive_nodes:
                ancestors |= set(node.get_descendants())
                ancestors.add(node)
        tree.prune(ancestors)
        return tree