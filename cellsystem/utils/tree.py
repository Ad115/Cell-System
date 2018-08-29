import ete3

class Tree:
    'Wrapper for the ETE Tree class with some extra conveniences.'
    
    def __init__(self, tree=None):
        if tree:
            # Initialize from a previous tree
            self.tree = tree.copy()
        else:
            # Initialize a new tree
            self.tree = ete3.Tree()
    # ---
    
    def __getattr__(self, name):
        'Delegate tree methods to the internal tree.'
        return getattr(self.tree, name)
    # ---
    
    def copy(self):
        'Make a copy of the tree.'
        return self.__class__(tree=self.tree)
    # ---
    
    def show(self, *args, inline=False, styling=None, savefig=None, **kwargs):
        "Display the tree."
        
        # Assemble the treestyle object
        ts = kwargs.get('tree_style', ete3.TreeStyle())
        
        kwargs['tree_style'] = ts
        
        # Check if a tree styling dict was specified
        if styling:
            for key,value in styling.items():
                setattr(ts, key, value)
                
                
        # Check if user wants to save the image
        if savefig:
            self.tree.render(savefig, *args, **kwargs)
        
        # Inline Jupyter output
        if inline:
            return self.tree.render('%%inline', *args, **kwargs)
        else:
            # Tree GUI rendering
            return self.tree.show(*args, **kwargs)
    # ---
    
    def prune_leaves(self, to_stay):
        'Prune tree branches to leave only the leaves in `to_stay`.'
        t = self.tree
        
        # Fetch leaf nodes with those names
        stay_nodes = set()
        for leaf in t:
            if leaf.name in to_stay:
                stay_nodes.add(leaf)
        
        t.prune(stay_nodes, preserve_branch_length=True)
        
        return self
    # ---
    
    def __str__(self):
        "A handy ASCII code representation of the tree."
        return self.tree.__str__()
    # ---
# --- Tree
