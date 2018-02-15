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
    
    def __iter__(self):
        "Generate the intermediate states."
        current_state = self.initial_state.copy()
        yield current_state.copy()
        
        for change in self.changes:
            # Decode change
            change_type = self._which_action(change)
            cell, other = change
            
            # Perform change
            if change_type == "migration":
                current_state[cell] = other
            else:
                del current_state[cell]
                
                if change_type == "division":
                    (d1, s1),(d2, s2) = other
                    current_state[d1] = s1
                    current_state[d2] = s2
                    
                elif change_type == "death": 
                    pass
        
            yield current_state.copy()
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
