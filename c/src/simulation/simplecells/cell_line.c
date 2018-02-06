 
/**
 * =========
 * Cell line
 * =========
 * 
 * Implementation file for the CellLine class, 
 * along with methods and auxiliary definitions.
 */

#include <stdlib.h>
#include <stdio.h>

#include "cell_line.h"
#include "cell/cell.h"



// ----- Main structure

// The structure is private and should not be accessed directly 
// from outside this file, but with the interface described in the 
// header file.  
struct CellLine_struct { /**
    Handles the specimens of a specific cell lineage.

    A cell lineage is a group of cells that have a common ancestor, we
    represent the common ancestor by it's ancestral genome.
    This structure is in charge of holding this ancestral code and managing
    the cells creating new cells when needed and cleaning up the dead ones.

    Atributes:
            + Ancestral genome: A string-like object.
            + Cells: The cells inherited from this cell line.
            + Current cell index: Each cell has a unique index. This is the
                                  index to place in the next cell to be born.
    */
    int current_index;
    List *cells;
};

typedef struct CellLine_struct CellLine;



// ----- Methods

CellLine *CellLine_new( ) { /**
    Creation of a cell lineage.
    */
    // Create
    CellLine *self = malloc(1 * sizeof(*self));
    // Initialize
    self->current_index = 0;
    self->cells = List_new();
        
    return self;
        
} // --- CellLine_new


void CellLine_del( CellLine *self ) { /**
    Deleter for a cell line object.
    */
    // 1 --- Delete the cells from this cell line
        List *cells = self->cells;
        
        for(int i=0; i < List_size(cells); i++) {
            // Fetch the ith cell
            Cell *item = List_at(cells, i);
            // Delete the cell
            Cell_del(item);
        }
        
        // Remove the list
        List_del(cells);
        
    // 2 --- Delete the cell line structure
        free(self);
        
} // --- CellLine_del


Cell *CellLine_new_cell( CellLine *self) { /**
    Get a new blank cell in this lineage and system.
    */
    // Fetch a fresh, new cell
    Cell *cell = Cell_new( self,              // Cell line
                           self->current_index ); // Index
        
    self->current_index += 1;
        
    // Add to the cells from this cell line
    List_push(self->cells, cell);
        
    return cell;
    
} // --- CellLine_new_cell


Cell *CellLine_recycle_cell(CellLine *self, 
                            Cell *cell, 
                            int father) { /**
    Clear previous information from a cell.
    */
    Cell_set_father(cell, father);
        
    Cell_set_index(cell, self->current_index);
        
    self->current_index += 1;
        
    return cell;
        
} // --- CellLine_recycle_cell


CellLine *CellLine_process( CellLine *self ) { /**
    Move a step forward in time.
    */
    List *cells = self->cells;
    int n = List_size(cells);
    
    for( int i=0; i<n; i++ ) {
        // Fetch the i_th cell
        Cell *cell = List_at(cells, i);
        // Process the cell
        Cell_process(cell);
    }
    
    return self;
            
} // --- CellLine_process


void CellLine_print( CellLine *self ) { /**
    Print the state of the cell line.
    */
    List *cells = self->cells;
    int n = List_size(cells);
    
    printf("<CellLine object. Cells: [");
    
    for( int i=0; i<n; i++ ) {
        // Fetch the i_th cell
        Cell *cell = List_at(cells, i);
        // Process the cell
        printf("%d, ", Cell_index(cell));
    }
    
    printf("]>");
    
} // --- CellLine_print
