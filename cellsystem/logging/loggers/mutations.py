from ete3 import Tree
from .weak import WeakLog

class MutationsLog(WeakLog):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mutations = Tree()
        self.alive = {}
        self.tmp = None
        
    def log_newcell(self, cell):
        self.alive[cell.index] = self.mutations\
                                    .add_child(name=cell.index)
        
    def preparefor_division(self, cell):
        self.tmp = cell.index
        
    def log_division(self, daughters):
        d1, d2 = daughters
        father = self.tmp
        node = self.alive[father]
        self.alive[d1.index] = node
        self.alive[d2.index] = node
        # Cleanup
        del self.alive[father]
        self.tmp = None
        
    def log_death(self, cell):
        # No further mutations, so no need to hold it
        del self.alive[cell.index]
        
    def log_mutation(self, cell):
        node = self.alive[cell.index]
        new = node.add_child(name=cell.genome)
        self.alive[cell.index] = new