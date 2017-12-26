import sys

class BaseLogger:
    "A logger class that works as a register of the actions of a cell system."
    
    def __init__(self, *args, **kwargs):
        pass
    # ---
    
    def preparefor(self, actionname, entity):
        'Save previous state before the entity takes the given action.'
        getattr(self, 'preparefor_'+actionname)(entity)
    # ---
        
    def log(self, actionname, *entities):
        'Log the action.'
        getattr(self, 'log_'+actionname)(*entities)
    # ---
# ---BaseLogger

class SimpleLogger(BaseLogger):
    'Simple logger that limits to print the action.'
    
    def preparefor_division(self, cell):
        print("Cell no. {} dividing @ {}".format(cell.index,
                                                 cell.coordinates))
        
    def log_division(self, daughter1, daughter2):
        print("\tNew cells: {} @ {} and {} @ {}".format(
                    daughter1.index,
                    daughter1.coordinates, 
                    daughter2.index, 
                    daughter2.coordinates))
        
    def log_death(self, cell):
        print("Cell no. {} dying @ site {} (father {})".format(
            cell.index, cell.coordinates, cell.father))
        
    def preparefor_migration(self, cell):
        print("Cell no. {} migrating from site {} (father {})".format(
                cell.index, cell.coordinates, cell.father))
        
    def log_migration(self, cell):
        print("\t New site: {}".format(cell.coordinates))
        
    def preparefor_mutation(self, cell):
        print("\t\t Initial mutations: {}\n \
               \t Initial genome: {}".format(cell.mutations, cell.genome))
        
    def log_mutation(self, cell):
        print("\t\t Final mutations: {}\n \
               \t Final genome: {}".format(cell.mutations, cell.genome))
        
from collections import defaultdict

class PhylogenyLogger(BaseLogger):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.phylogeny = defaultdict(list)
        self.tmp = None
        
        
    def preparefor_division(self, cell):
        self.tmp = cell.index
        
    def log_division(self, daughter1, daughter2):
        father = self.tmp
        self.phylogeny[father].append(daughter1.index)
        self.phylogeny[father].append(daughter2.index)
        self.tmp = None
        
    def log_death(self, cell):
        pass
        
    def preparefor_migration(self, cell):
        pass
        
    def log_migration(self, cell):
        pass
        
    def preparefor_mutation(self, cell):
        pass
        
    def log_mutation(self, cell):
        pass
        
from ete3 import Tree
class AncestryLogger(BaseLogger):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.phylogeny = Tree()
        self.nodes = {0:self.phylogeny}
        self.tmp = None
        
        
    def preparefor_division(self, cell):
        self.tmp = cell.index
        
    def log_division(self, daughter1, daughter2):
        father = self.tmp
        self.nodes[daughter1.index] = self.nodes[father].add_child(name = daughter1.index)
        self.nodes[daughter2.index] = self.nodes[father].add_child(name = daughter2.index)
        del self.nodes[father]
        self.tmp = None
        
    def log_death(self, cell):
        # No further childs, so no need to hold it
        del self.nodes[cell.index]
        
    def preparefor_migration(self, cell):
        pass
        
    def log_migration(self, cell):
        pass
        
    def preparefor_mutation(self, cell):
        pass
        
    def log_mutation(self, cell):
        pass

    
    
class MutationsLogger(BaseLogger):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mutations = Tree()
        self.nodes = {0:self.mutations}
        self.tmp = None
        
        
    def preparefor_division(self, cell):
        self.tmp = cell.index
        
    def log_division(self, daughter1, daughter2):
        father = self.tmp
        node = self.nodes[father]
        self.nodes[daughter1.index] = node
        self.nodes[daughter2.index] = node
        # Cleanup
        del self.nodes[father]
        self.tmp = None
        
    def log_death(self, cell):
        # No further mutations, so no need to hold it
        del self.nodes[cell.index]
        
    def preparefor_migration(self, cell):
        pass
        
    def log_migration(self, cell):
        pass
        
    def preparefor_mutation(self, cell):
        pass
        
    def log_mutation(self, cell):
        node = self.nodes[cell.index]
        new = node.add_child()
        self.nodes[cell.index] = new
        

class Logger(BaseLogger):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mutations = MutationsLogger()
        self.ancestry = AncestryLogger()
        
    def preparefor(self, actionname, entity):
        'Save previous state before the entity takes the given action.'
        getattr(self.mutations, 'preparefor_'+actionname)(entity)
        getattr(self.ancestry, 'preparefor_'+actionname)(entity)
    # ---
        
    def log(self, actionname, *entities):
        'Log the action.'
        getattr(self.mutations, 'log_'+actionname)(*entities)
        getattr(self.ancestry, 'log_'+actionname)(*entities)
    # ---

