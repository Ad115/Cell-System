#include <stdio.h>

#include "simulation/simplecells/cell_line.h"



int main() {
    // Create a new cell line
    CellLine *cells = CellLine_new();
    printf("Cell line: \n");
    CellLine_print(cells);
    
    // Create the first cell
    Cell *cell = CellLine_new_cell(cells);
    printf("\nFirst cell: \n");
    Cell_print(cell);
    
    // Let it take an action
    ActionResult *result = Cell_process(cell);
    // Decompose 
    Cell *d1 = ActionResult_pop_cell(result);
    Cell *d2 = ActionResult_pop_cell(result);
    // Print
    printf("\nAfter division, cells are: ");
    Cell_print(d1);
    printf(" and ");
    Cell_print(d2);
    
    // Let every cell take an action
    CellLine_process(cells);
    
    // How is the system now?
    printf("\n");
    CellLine_print(cells);
    printf("\n");
    
    // Cleanup
    CellLine_del(cells);
    
    return 0;
}
