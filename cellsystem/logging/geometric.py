"""
Geometric Logging
=================

This module defines functionality for following the geometric
evolution of the cell blob through time.

The classes GeometricLog and WorldLines are defined here.
"""

from collections import defaultdict

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from .core import WeakLog


class GeometricLog(WeakLog):
    """Registers the geometric positions of the cells."""

    def __init__(self, *args, **kwargs):
        """Maintains a changes record."""
        # Init as the superclass (Weak)
        super().__init__()
        
        self.initial_state = dict()
        self.changes = []
    # ---
    
    def _unpack_info(self, cell):
        'Unpack cell information.'
        index = cell.index
        site = cell.coordinates
        
        return index, site
    # ---
    
    def _register(self, cell):
        "Add the cell's current information to the changes."
        index, site = self._unpack_info(cell)
        self.changes.append( (index, site) )
    # ---
        
    def _which_action(self, change):
        "Decode the event into a concrete action."
        
        # There are 3 possible actions: 
        #   division: ( father, ((d1,site), (d2,site)) )
        #   death: (cell, None)
        #   and migration: (cell, site)
        cell, other = change
        if other is None:
            return "death"
        
        else:
            # Check division
            try:
                (d1, site), (d2, site) = other
                return "division"
            # Check migration
            except TypeError:
                return "migration"
    # ---
    
    def iter_changes(self):
        "Iterate through every action"        
        for change in self.changes:
            # Decode change
            change_type = self._which_action(change)
        
            yield change_type, change
    # ---
    
    def iter_states(self):
        "Generate the intermediate states."
        current_state = self.initial_state.copy()
        yield current_state.copy()
        
        for change_type, change in self.iter_changes():
            # Perform change
            if change_type == "migration":
                cell, site = change
                current_state[cell] = site
                
            elif change_type == "division":
                # Unpack
                cell, daughters = change
                del current_state[cell]
                
                (d1, s1),(d2, s2) = daughters
                current_state[d1] = s1
                current_state[d2] = s2
                    
            elif change_type == "death": 
                cell, _ = change
                del current_state[cell]
        
            yield current_state.copy()
    # ---
    
    def worldlines(self, prune_death=False):
        "Get the geometric evolution of individual cells in space and time."
        return WorldLines.from_log(self, prune_death)
    # ---
        
    def log_newcell(self, cell):
        
        self._register(cell)
    # ---
    
    def preparefor_division(self, cell):
        # The index of the dividing cell
        self.tmp = cell.index
    # ---
    
    def log_division(self, daughters):
        # Register the disappeareance of the father
        father = self.tmp
    
        # Register the sites of the daughters
        d1, d2 = daughters
        d1_info = self._unpack_info(d1)
        d2_info = self._unpack_info(d2)
        
        self.changes.append( (father, (d1_info, d2_info)) )
    # ---
    
    def log_migration(self, cell):
        
        self._register(cell)
    # ---
    
    def log_death(self, cell):
        "Register the disappeareance of the cell."
        self.changes.append( (cell.index, None) )
    # ---
    
    
    
class WorldLines:
    """A class that represents the worldlines of a set of cells.
    
    A worldline is the place in time and space that a cell occupies throughout
    it's existence.
    """
    
    def __init__(self, initial_state=None, time=0):
        "Initialize from a state."
        if initial_state is None:
            initial_state = dict()
        
        self.worldlines = defaultdict(list)
        # Assemble initial state
        for cell,site in initial_state.items():
            # A point in spacetime
            event = self._event(time, site)
            
            self.worldlines[cell].append(event)
    # ---
    
    @staticmethod
    def _event(time, site):
        "Assemble a point in spacetime."
        return tuple( [time]+list(site) )
    # ---
    
    @classmethod
    def from_log(cls, geometric_log, prune_death=False):
        "Initialize from a geometric log."
        changes = geometric_log.iter_changes()
        states = geometric_log.iter_states()
        
        # Intialize timelines object
        current_state = next(states)
        t = 0
        worldlines = cls(current_state, t)
        
        # Assemble timelines
        for i,(state,change) in enumerate(zip(states, changes)):
            
            worldlines.update(state, 
                              transition=change, 
                              time=i+1, 
                              prune_death=prune_death)
        
        return worldlines
    # ---
    
    def update(self, state, transition, time, prune_death=False):
        "Add the event described by the transition, time and final state."
        change_type, change = transition
        
        if prune_death and (change_type == "death"):
            # Cell is dead, remove it's timeline
            cell, _ = change
            self.remove(cell)
            
        elif change_type == "division":
            cell, daughters = change
            (d1, s1),(d2, s2) = daughters
            # Find the time and site of the division
            division = self.last_state_of(cell)
            # The daughters' timeline starts at the 
            # site of the division and to their current site
            self.add_event(d1, division)\
                .add_event(d2, division)
            
        for cell, site in state.items():
            self.add_event(cell, self._event(time, site))
            
        return self
    # ---
    
    def remove(self, cell):
        "Remove the given cell's timeline."
        del self.worldlines[cell]
    # ---
    
    def last_state_of(self, cell):
        "Return the last recorded event of the given cell."
        return self.worldlines[cell][-1]
    # ---
    
    def add_event(self, cell, event):
        "Add an event (a spacetime coordinate) for the cell."
        self.worldlines[cell].append(event)
        return self
    # ---
    
    def __getitem__(self, cell):
        "Get the timeline of a cell."
        return self.worldlines[cell]
    # ---
    
    def __iter__(self):
        "Iterate through the cell worldlines."
        yield from self.worldlines.items()
    # ---
    
    def show(self):
        "Render the 3D worldlines as a plot."
        fig = plt.figure()
        ax = fig.gca(projection='3d')

        for cell,timeline in self:
            t, x, y = zip(*timeline)
            ax.plot(t, x, y)
            ax.scatter(t[0], x[0], y[0], marker='o')   # End point
            ax.set_xlabel('t')
            ax.set_ylabel('x')
            ax.set_zlabel('y')
        plt.show()
    # ---
# --- WorldLines
