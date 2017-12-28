from ete3 import Tree
from .weak import WeakLog

class AncestryLog(WeakLog):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ancestry = Tree()
        self.alive = {}
        self.tmp = None
    
    def log_newcell(self, cell):
        self.alive[cell.index] = self.ancestry\
                                    .add_child(name=cell.index)
        
    def preparefor_division(self, cell):
        self.tmp = cell.index
        
    def log_division(self, daughters):
        d1, d2 = daughters
        father = self.tmp
        self.alive[d1.index] = self.alive[father]\
                                .add_child(name=d1.index)
        self.alive[d2.index] = self.alive[father]\
                                .add_child(name=d2.index)
        del self.alive[father]
        self.tmp = None
        
    def log_death(self, cell):
        # No further childs, no need to track
        del self.alive[cell.index]