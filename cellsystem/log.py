import sys

class BaseLogger:
    "A logger class that works as a register of the actions of a cell system."
    
    def __init__(self, file=sys.stdout):
        self.file = file
        self.preparation = {}
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
        
        
        
        
    
