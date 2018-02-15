from .core import Log

class SimpleLog(Log):
    'Simple logger that limits to print the action.'
    
    def preparefor_division(self, cell):
        print("Cell no. {} dividing @ {}".format(cell.index,
                                                 cell.coordinates))
        
    def log_division(self, daughters):
        daughter1, daughter2 = daughters
        print("\tNew cells: {} @ {} and {} @ {}".format(
                    daughter1.index,
                    daughter1.coordinates, 
                    daughter2.index, 
                    daughter2.coordinates))
        
    def preparefor_death(self, cell):
        pass
        
    def log_death(self, cell):
        print("Cell no. {} death @ site {} (father {})".format(
            cell.index, cell.coordinates, cell.father))
        
    def preparefor_migration(self, cell):
        print("Cell no. {} migrating from site {} (father {})".format(
                cell.index, cell.coordinates, cell.father))
        
    def log_migration(self, cell):
        print("\t New site: {}".format(cell.coordinates))
        
    def preparefor_mutation(self, cell):
        print("Cell no. {} mutating @ site {} (father {})".format(
            cell.index, cell.coordinates, cell.father))
        print("\t\t Initial mutations: {}\n \
               \t Initial genome: {}".format(cell.mutations, cell.genome))
        
    def log_mutation(self, cell):
        print("\t\t Final mutations: {}\n \
               \t Final genome: {}".format(cell.mutations, cell.genome))
        
    def log_newcell(self, cell):
        print( "New cell {} added @ {}".format(cell.index, cell.coordinates) )
# --- SimpleLogger 
