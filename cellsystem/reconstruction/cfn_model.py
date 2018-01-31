"""
Module implementing the Cavender-Farris-Neymann stochastic tree model.

The model is based on the description by the book:
    
    Computational Phylogenetics.
      An introduction to designing methods for phylogeny estimation.
      -- by Tandy Warnow
      
Usage:

```python
# Create a new empty tree.
cfn = CFN_Tree()

# Branch randomly until you have 5 leaves.
cfn.populate(5)

    # Node: 0, node probability: 0
    # Node: 1, node probability: 0.2192846999188683
    # Node: 2, node probability: 0.06144844447962278
    # Node: 3, node probability: 0.14342505932071808
    # Node: 4, node probability: 0.1370117188846906
    # Node: 5, node probability: 0.44060196062669255
    # Node: 6, node probability: 0.009555798385131098
    # Node: 7, node probability: 0.48946332859444935
    # Node: 8, node probability: 0.39505550345399304
    #
    #       /-3
    #    /1|
    #   |  |   /-7
    #   |   \4|
    # -0|      \-8
    #   |
    #   |   /-5
    #    \2|
    #       \-6

# Evolve 5 traits through the tree
sequences = cfn.evolve_traits([1,1,1,1,1])
print(sequences)

    # { 3: [0, 0, 0, 1, 1], 
    #   7: [1, 0, 1, 0, 1], 
    #   8: [1, 0, 0, 1, 1], 
    #   5: [1, 1, 1, 1, 1], 
    #   6: [1, 1, 1, 1, 1] }


```

The CFN model in words from the book:

"The Cavender-Farris-Neyman (CFN) model describes how a trait (which 
 can either be present or absent) evolves down a tree (Cavender, 
 1978; Farris, 1973; Neyman, 1971).

 ...a CFN model has a rooted binary tree T (i.e., a tree in which 
 every node is either a leaf or has two children) with numerical 
 parameters that describe the evolutionary process of a trait. Under 
 the CFN model, the probability of absence (0) or presence (1) is the 
 same at the root, but the state can change on the edges (also called 
 branches) of the tree. Thus, we associate a parameter p(e) to every 
 edge e in the tree, where p(e) denotes the probability that the 
 endpoints of the edge e have different states. In other words, p(e)
 is the probability of changing state (from 1 to 0, or vice-versa)
 ... we require 0 < p(e) < 0.5.

 Under  the  CFN  model,  a  trait  (which  is  also  called  a  
 “character”)  evolves  down  the tree under this random process, and 
 hence attains a state at every node in the tree, and in particular 
 at the leaves of the tree. You could write a computer program for a 
 CFN model tree that would generate 0s and 1s at the leaves of the 
 tree; thus, CFN is a generative model.
 
 Each time you ran the program you would get another pattern of 0s and 
 1s at the leaves of the tree. Thus, if you repeated the process 10 
 times, each time independently generating a new trait down the tree, 
 you would produce sequences of length 10 at the leaves of the tree."
    -- from the book.
"""

import ete3 as ete
import random as rnd
from collections import defaultdict


def swap(binary):
    if binary:
        return 0
    else:
        return 1
# ---


def random_test(probability):
    'Return True with a given probability, otherwise return False.'
    return (rnd.random() < probability)
# ---


class CFN_Tree(ete.Tree):
    "A Cavender-Farris-Neymann stochastic tree model."
    
    def populate(self, n):
        'Populate the tree with nodes and change probabilities.'
        # Populate the usual way
        super().populate(n)
        # Change names and add probabilities
        for i,node in enumerate(self.traverse()):
            node.name = i
            if i > 0:
                # Add a change probability < 0.5
                node.add_feature('probability', rnd.random()/2)
                # The probability must be associated to the edge (branch),
                # in this implementation, we associate the probability to
                # the node downstream of the edge.
            else:
                # No probability of change before this
                node.add_feature('probability', 0)
            print(f"Node: {i}, node probability: {node.probability}")
        print(self)
    # ---        
        
    def total_nodes(self):
        return len(list(self.traverse()))
    # ---
    
    def evolve_traits(self, traits):
        "Evolve the binary traits through the tree."
        # The sequences generated
        sequences = defaultdict(list)
        for leaf in self.iter_leaves():
            path_from_root = list(reversed(leaf.get_ancestors()))
            path_from_root.append(leaf)
            # Evolve each trait
            for trait in traits:
                # Follow path stochastically 
                final_trait = self.trait_traverse(path_from_root, trait)
                # Save character's final state
                sequences[leaf.name].append(final_trait)
        return dict(sequences)
    # ---
            
    def trait_traverse(self, path_from_root, init):
        # Follow path stochastically 
        trait = init
        for node in path_from_root: 
            probability = node.probability
            if random_test(probability):
                trait = swap(trait)
        # Return character's final state
        return trait
    # ---
    
    def __str__(self):
        return self.get_ascii(show_internal=True)
    # ---
# --- CFN_Tree