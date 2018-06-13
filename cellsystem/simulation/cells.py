"""

Structures representing the biological entities.
"""

import numpy as np
import random
from functools import wraps

from ..logging import logged
from .action import Action



def behavior(actionname, actionfn=None, probability=None, prepare=True):
    """Assemble a cell behavior.
    
    Adds logging and asociates a name and a probability function
    to the raw action function. Allows to specify if the logging of 
    the action requires to prepare the log.
    
    Can be used as a function decorator or as a normal function.
    """
    # Auxiliary function
    def make_behavior(actionfn):
        """Decorated action."""
        # Add logging
        logged_action = logged(actionname, prepare=prepare)(actionfn)
        
        return Action(logged_action,
                      probability, 
                      actionname ) 
    # ---
    
    if actionfn:
        # Used as a function
        return make_behavior(actionfn)
    else:
        # Used as a decorator
        return make_behavior    
# ---
    
    

class Cell:
    """
    A single cell.

    It acts according to it's state, and the states of nearby cells and sites.

    Attributes:
        + Index: A label that identifies it among others in the
                 same lineage.
        + Father: The index (lineage label) of it's father.
        + CellLine: The lineage this cell belongs to.
        + Site: The place in the grid this cell inhabits in.
        + Mutations: The mutations in this cell relative to the cell
                     lineage's reference

    """

    def __init__(self, lineage, index):
        """Create a new cell.

        Parameters:
            :param cell_line: The lineage this cell belongs to.
            :param index: The ID of this cell in the lineage.

        """
        self.index = index
        self.lineage = lineage
        self.father = None
        self.site = None
        self.actions = self.lineage.fetch_behaviors()
        self.mutations = []
    # ---

    @property
    def coordinates(self):
        """Coordinates of the site that the cell inhabits."""
        return self.site.coordinates

    @property
    def mutations(self):
        """Record of the mutations the cell has had.

        The mutations are relative to the ancestral genome.

        """
        return self._mutations

    @mutations.setter
    def mutations(self, value):
        """Setter for the cell's mutations."""
        self._mutations = list(value)  # COPY
    # ---

    @property
    def ancestral_genome(self):
        """Ancestral genome of the cell lineage."""
        return self.lineage.genome
    # ---

    @property
    def genome(self):
        """Genome of the cell.

        It is assembled from the cell's ancestral genome and it's mutations.

        """
        # Get the original genome
        bases = list(self.ancestral_genome)
        # Add mutations one by one
        for position, mutated in self.mutations:
            bases[position] = mutated
        # Assemble the final genome
        genome = ''.join(bases)

        return genome
    # ---
    
    @property
    def genome_alphabet(self):
        """Genome alphabet of the cell line.

        The set of characters a genome is composed of.
        (The genome characters may really represent genes, aminoacids, etc...)

        """
        return self.lineage.genome_alphabet
    # ---

    def initialize(self, site=None, father=None, mutations=None):
        """Initialize grid site, mutations and father."""
        if site:
            self.site = site
        if father:
            self.father = father
        if mutations:
            self.mutations = mutations  # copy
    # ---
    
    def add_mutation(self, position, mutated):
        """Add a mutation to the cell in the given position of the genome.
        
        Note: The genome may not represent a nucleotide sequence, so these
        mutations may not represent SNPs.
        """
        mutation = (position, mutated)
        self.mutations.append(mutation)
    # ---

    def new_daughter(self):
        """Initialize a new daughter cell.

        Initialize with father and mutation attributes.

        """
        daughter = self.lineage.new_cell()
        daughter.initialize( father=self.index,
                             mutations=self.mutations )
        return daughter
    # ---

    def add_to(self, site):
        """Add the cell to the site."""
        self.site = site
        site.add_guest(self)
    # ---    
    
    def choose_action(self, actions, weights):
        "Select an action with the probability given by the weights."
        r = random.random()
        sum = 0
        
        for w, action in zip(weights, actions):
            sum += w
            if sum >= r:
                break
        return action
    # ---   

    def process(self, *args, **kwargs):
        """Select an action and perform it."""
        # Select an action
        actions, weights = self.actions
        action = self.choose_action(actions, weights)
        
        # Perform the action according to it's respective probability
        p = action.probability(self)
        action.try_action(self, *args, probability=p, **kwargs)
    # ---
# --- Cell



class CellLine:
    """
    Handles the specimens of a specific cell lineage.

    A cell lineage is a group of cells that have a common ancestor, we
    represent the common ancestor by it's ancestral genome.
    This structure is in charge of holding this ancestral code and managing
    the cells creating new cells when needed and cleaning up the dead ones.

    Atributes:
            + Ancestral genome: A string-like object.
            + Cells: The cells inherited from this cell line.
            + Alive/Dead cells.
            + Current cell index: Each cell has a unique index. This is the
                                  index to place in the next cell to be born.

    """

    def __init__(self,
                 *args,
                 genome=None,
                 genome_alphabet=None,
                 recycle_dead=True,
                 **kwargs):
        """Creation of a cell lineage.

        Parameters:
            :param genome: (default 'AAAAAAAAAA') Sequence representing the 
                            base genome of the cells from this line.
            :param recycle_dead: (default True) Repurpose dead cells when needed,
                                 this helps improve memory usage.

            If a custom genome is passed, the genome alphabet should be
            passed too unless it is formed of the letters in "ACGT".
            
        """
        self.recycle_dead = recycle_dead
        self.current_index = 0
        self.cells = []
        self.alive_cells = set()
        self.dead_cells = set()
        self.behaviors = {'actions': [],
                          'weights': [],
                          'normalized_weights': []}
        
        if genome is None:
            genome = 10 * 'A'
        self.genome = genome
        
        if genome_alphabet is None:
            genome_alphabet = 'AGCT'
        self.genome_alphabet = genome_alphabet
    # ---
        
    @property
    def total_cells(self):
        return len(self.alive_cells)
    # ---
    
    def fetch_behaviors(self):
        "The behaviors that the cells in this lineage perform."
            
        return ( list(self.behaviors['actions']), 
                 list(self.behaviors['normalized_weights']) )
    # ---
    
    def add_behaviors(self, behaviors, weights=None):
        """Add the behaviors defining the cells from this cell line.
        
        Params:
           
            behaviors (list of callables):
                The list of actions that the cells in this
                lineage will be able to perform.
               
            weights (optional list of numeric values):
                The list of relative weights for selecting each action.
                The bigger the weight of an action relative to the weights 
                of the others, the more likely is that that action will be
                selected by the cell at each step. default is all actions
                have the same weights.
                
        Raises:
            
            ValueError:
                If the weights are not of the same length as the behaviors.
            
        """
        if weights:
            if len(weights) != len(behaviors):
                raise ValueError('Weights must correspond to behaviors one-to-one.')
        else:
            # All actions have the same weight
            weights = [1] * len(behaviors)
            
        self.behaviors['actions'] += behaviors
        self.behaviors['weights'] += weights
        
        # Ensure normalization
        all_weights = self.behaviors['weights']
        total_w = sum(all_weights)
        self.behaviors['normalized_weights'] = [w/total_w for w in all_weights]
    # ---

    def new_cell(self):
        "Get a new blank cell in this lineage and system."
        # Fetch a blank cell
        if self.recycle_dead and self.dead_cells:
            # Fetch a dead cell to recycle
            new = self.cell_to_recycle()
            self.recycle_cell(new)
        else:
            # Fetch a fresh, new cell
            new = Cell( lineage = self,
                        index = self.current_index )
            self.current_index += 1
            self.cells.append(new)

        # Update state to take new cell into account
        self.alive_cells.add(new)
        return new
    # ---

    def cell_to_recycle(self):
        """Return a cell from the dead ones."""
        recycle = self.dead_cells.pop()
        return recycle
    # ---

    def recycle_cell(self, cell):
        """Clear previous information from a cell."""
        # Place new ID
        cell.index = self.current_index
        self.current_index += 1
    # ---

    def sample(self, all=False, n=1):
        """Take a sample of alive cells.

        :param all: If True, return all alive cells, else, return a sample of
                    size n.
        :param n: The size of the sample. If 1, return the cell without a
                  container.

        """
        # If it is asked for all cells,
        # take a sample of the whole size
        if all:
            n = len(self.alive_cells)
        # Return a sample of size n
        return random.sample(self.alive_cells, n)
    # ---

    def handle_death(self, dying):
        """Process a dying cell.

        This means removing from the alive cells and adding to the dead ones,
        maybe to recycle it when another is born.

        """
        self.alive_cells.remove(dying)
        self.dead_cells.add(dying)
    # ---
        
    def process(self, *args, **kwargs):
        'Move a step forward in time.'
        for cell in self.sample(all=True):
            cell.process(*args, **kwargs)
    # ---
# --- CellLine
