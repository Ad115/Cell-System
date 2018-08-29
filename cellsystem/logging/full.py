from .core import MultiLog
from .geometric import GeometricLog
from .treelogs import MutationsLog, AncestryLog
from .printer import PrinterLog

class FullLog(MultiLog):
    """An aggregate log that records geometric information, 
    mutations, ancestry and prints the actions to the screen.
    (Technically is a multilog that contains a GeometricLog,
    a MutationsLog, an AncestryLog and a PrinterLog.)
    
    Each part can be accesed with::
    
        log[{{logname}}]
    
    where {{logname}} can be one of: 'geometry', 'mutations', 
    'ancestry' or 'printer'.
    
    also, each log can be (de)activated with::
    
        # Deactivate log
        log[{{logname}}].silence()
        
        # Reactivate log
        log[{{logname}}].activate()
        
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Register the relevant logs
        self.register(GeometricLog(), name='geometry')
        self.register(MutationsLog(), name='mutations')
        self.register(AncestryLog(), name='ancestry')
        self.register(PrinterLog(), name='printer')
    # ---
    
    def worldlines(self, prune_death=False):
        "Fetch information of the cells' evolution in space and time."
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
