from .core import MultiLog
from .geometric import GeometricLog
from .treelogs import MutationsLog, AncestryLog
from .simple import SimpleLog

class FullLog(MultiLog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Register the relevant logs
        self.register(GeometricLog(), name='geometry')
        self.register(MutationsLog(), name='mutations')
        self.register(AncestryLog(), name='ancestry')
        self.register(SimpleLog(), name='simple')
    # ---
    
    
    def geometry(self, prune_death=False):
        "Fetch information of the cells' dynamic in physical space."
        return self.logs['geometry'].worldlines(prune_death)
    # ---
    
    def mutations(self, prune_death=False):
        "Fetch information of the cells' mutational history."
        return self.logs['mutations'].fetch_tree(prune_death)
    # ---
    
    def ancestry(self, prune_death=False):
        "Fetch information of the cells' \"family tree\"."
        return self.logs['ancestry'].fetch_tree(prune_death)
    # ---
# --- FullLog
