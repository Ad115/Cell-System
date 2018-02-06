/**
 * ===================
 * Cell action result
 * ===================
 * 
 * Implementation file for the ActionResult class,
 * along with methods and auxiliary definitions.
 */

#include <stdlib.h>

#include "action_result.h"
#include "../../../utilities/list.h"



// ----- Main structure
// The structure is private and should not be accessed directly 
// from outside this file, but with the interface described in the 
// header file. 
struct ActionResult_struct { /*
    
    Cell action result.

    Represents the result of a computation on a biological entity.
    
    Is only a wrapper on a list of cells, sites, nutrient, or mutations information.
    
    */
    List *cells; // The cells affected.
}; 

typedef struct ActionResult_struct ActionResult;



// ----- Methods

ActionResult *ActionResult_new() { /**
    New cell action result object.

    It is initialized with a function that when called will make
    the cell perform the action and a function that when called will
    calculate the probability to perform the action.

    */
    // Create
    ActionResult *self = malloc(1 * sizeof(*self));
    // Initialize
    self->cells = List_new();
    
    return self;
    
} // --- CellAction_new

void ActionResult_del( ActionResult *self ) { /**
    Deleter for an action object.
    */
    // Delete the cells list
    List_del( self->cells );
    // Delete the action result structure
    free(self);
}

ActionResult *ActionResult_add_cell( ActionResult *self, Cell *cell ) { /**
    Perform the action according to it's probability.
    */
    List_push( self->cells, cell );
    
    return self;
    
} // --- ActionResult_push_cell

Cell *ActionResult_pop_cell( ActionResult *self ) { /**
    Remove the last cell and return it.
    */
    
    return List_pop( self->cells );
    
} // --- ActionResult_push_cell

ActionResult *ActionResult_empty( ActionResult *self ) { /**
    Clear the state of the structure.
    */
    
    List_empty( self->cells );
    
    return self;
    
} // --- ActionResult_empty


