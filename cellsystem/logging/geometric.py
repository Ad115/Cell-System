from collections import defaultdict

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
    
    def get_timelines(self):
        "Get the geometric evolution of individual cells."
        states = self.iter_states()
        current_state = next(states)
        t = 0
        
        timelines = defaultdict(list, 
                                {cell:[(t,*site)] for cell,site 
                                       in current_state.items()})
        
        for i,(state,change) in enumerate(zip(states, self.iter_changes())):
            # Decode change
            change_type, change = change
            t = i+1
            
            if change_type == "division":
                cell, daughters = change
                (d1, s1),(d2, s2) = daughters
                # Find the time and site of the division
                division = timelines[cell][-1]
                # The daughters' timeline starts at the 
                # site of the division and to their current site
                timelines[d1].append( division )
                timelines[d2].append( division )
                
            for cell, site in state.items():
                    timelines[cell].append( (t, *site) )
        
        return timelines
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
