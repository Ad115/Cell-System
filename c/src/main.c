#include <stdio.h>

#include "simulation/simplecells/cell_line.h"
#include "simulation/simplecells/cell/cell.h"
#include "simulation/simplecells/cell/action_result.h"



int main() {
    // Create a new cell line
    CellLine *cells = CellLine_new();
    printf("New cell line created: \n");
    CellLine_print(cells);
    
    // Create the first cell
    printf("\n\nThe first cell of the cell line: \n");
    Cell *cell = CellLine_new_cell(cells);
    Cell_print(cell);
    
    // Let it take an action
    printf("\n\nNow, the cell will take an action:");
    ActionResult *result = Cell_process(cell);
    // Decompose 
    Cell *d1 = ActionResult_pop_cell(result);
    Cell *d2 = ActionResult_pop_cell(result);
    // Print
    printf("\nThe cell has divided into: ");
    Cell_print(d1);
    printf(" and ");
    Cell_print(d2);
    
    // Let every cell take an action
    printf("\n\nNow, let the system process every cell...\n");
    CellLine_process(cells);
    
    // How is the system now?
    printf("How is the system now?\n");
    CellLine_print(cells);
    printf("\n");
    
    // Cleanup
    CellLine_del(cells);
    
    return 0;
}
