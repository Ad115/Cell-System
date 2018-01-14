from ete3 import Tree, TreeStyle
from .weak import WeakLog

class TreeLog(WeakLog):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = Tree()
        self.alive = {}
        self.tmp = None
        
    def log_newcell(self, cell):
        self.alive[cell.index] = self.tree\
                                    .add_child(name=cell.index)
        
    def preparefor_division(self, cell):
        self.tmp = cell.index

    def log_death(self, cell):
        # No further mutations, so no need to hold it
        del self.alive[cell.index]
        
    @property
    def alive_nodes(self):
        return self.alive.values()
# ---

    
class AncestryLog(TreeLog):
        
    def log_division(self, daughters):
        'Add 2 new branches to the father of the cells.'
        d1, d2 = daughters
        father = self.tmp
        self.alive[d1.index] = self.alive[father]\
                                .add_child(name=d1.index)
        self.alive[d2.index] = self.alive[father]\
                                .add_child(name=d2.index)
        del self.alive[father]
        self.tmp = None
# ---


class MutationsLog(TreeLog):

    def log_division(self, daughters):
        'Remove the father from the alive cells.'
        d1, d2 = daughters
        father = self.tmp
        node = self.alive[father]
        self.alive[d1.index] = node
        self.alive[d2.index] = node
        # Cleanup
        del self.alive[father]
        self.tmp = None
        
    def log_mutation(self, cell):
        'Add a new child to the parent genome.'
        node = self.alive[cell.index]
        new = node.add_child(name=cell.genome)
        self.alive[cell.index] = new
# ---