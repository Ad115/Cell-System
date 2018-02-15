from ..utils import Tree
from .core import WeakLog

class TreeLog(WeakLog):
    'Base class for logs that grow trees.'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = Tree()
        self.alive = dict()
        self.tmp = None
    # ---
        
    @property
    def alive_nodes(self):
        return self.alive.values()
    # ---
    
    def add_child(self, parent=None, name=None):
        # Select node
        if parent is None:
            parent_node = self.tree
        else:
            parent_node = self.alive[parent]
            
        # Add child to the current node
        child = parent_node.add_child(name=str(name))
        
        return child
    # ---
    
    def fetch_tree(self, prune_death=False):
        """Fetch a copy of the tree.
        
        If `prune_death` is True, remove the leaves 
        that correspond to death cells.
        """
        # Make a copy of the tree
        original = self.tree
        t = original.copy()
        
        # Remove death cells.
        if prune_death:
            alive = { node.name for node in self.alive_nodes }
            t.prune_leaves(to_stay=alive)
            
        return t
    # ---
        
    def preparefor_division(self, cell):
        # Save the previous cell state
        self.tmp = cell.index
    # ---

    def log_death(self, cell):
        # No need to keep tracking
        del self.alive[cell.index]
    # ---
# --- TreeLog

    
class AncestryLog(TreeLog):
    """A tree log that maintains a \"family tree\".
    
    Each leaf represents a cell. When that cell divides,
    the leaf branches into leaves representing the daughters.
    
    """
    def add_child(self, *args, **kwargs):
        # First add the node normally to the tree
        child_node = super().add_child(*args, **kwargs)
        # Then register the new cell node
        # in the alive cells
        self.alive[kwargs['name']] = child_node
    # ---
    
    def log_newcell(self, cell):
        # Add a new child to the tree
        self.add_child(name=cell.index)
    # ---
        
    def log_division(self, daughters):
        'Add 2 new branches to the father of the cells.'
        d1, d2 = daughters
        father = self.tmp
        
        # Create new tree nodes
        self.add_child(father, name=d1.index)
        self.add_child(father, name=d2.index)
        
        # Cleanup
        del self.alive[father]
        self.tmp = None
    # ---
# --- AncestryLog


class MutationsLog(TreeLog):
    """A tree log that maintains a record of genome branching events.
    
    Each leaf represents a genome that may be present in one or more
    cells. When one of those cells mutates, the new genome is added as
    a child of that leaf. 
    """
    
    def log_newcell(self, cell):
        # Add a new child to the tree
        child = self.add_child(name=cell.genome)
        # Register cell as alive representative for the genome node
        self.alive[cell.index] = child
    # ---

    def log_division(self, daughters):
        'Remove the father from the alive cells.'
        d1, d2 = daughters
        father = self.tmp
        
        # Replace the genome representative.
        # Now the daughter cells are representatives
        # as having the genome of the father.
        genome_node = self.alive[father]
        self.alive[d1.index] = genome_node
        self.alive[d2.index] = genome_node
        
        # Cleanup
        del self.alive[father]
        self.tmp = None
    # ---
        
    def log_mutation(self, cell):
        'Add a new child to the parent genome.'
        child = self.add_child(cell.index, name=cell.genome) # New genome
        # Register cell as an alive representative 
        # for the genome node
        self.alive[cell.index] = child
    # ---
# --- MutationsLog
