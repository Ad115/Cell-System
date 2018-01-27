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
    # Node: 1, node probability: 0.45158852704268865
    # Node: 2, node probability: 0.11424818655999902
    # Node: 3, node probability: 0.4264051970154286
    # Node: 4, node probability: 0.459742963797842
    # Node: 5, node probability: 0.3654757150714647
    # Node: 6, node probability: 0.4320439824130711
    # Node: 7, node probability: 0.4988182678649847
    # Node: 8, node probability: 0.11885743478646316
    #
    #          /-7
    #       /-|
    #    /-|   \-8
    #   |  |
    # --|   \-4
    #   |
    #   |   /-5
    #    \-|
    #       \-6

# Evolve 5 traits through the tree
sequences = cfn.evolve_traits([1,1,1,1,1])
print(sequences)

    # { 3: [1, 0, 0, 0, 1],
    #   5: [1, 1, 1, 1, 1],
    #   6: [1, 1, 0, 1, 1],
    #   7: [1, 0, 0, 1, 1],
    #   8: [1, 1, 1, 1, 1] }

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
 is the probability of changing state (from 1 to 0, or vice-versa).

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
                # Add a change probability >= 0.5
                node.add_feature('probability', rnd.random()/2)
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