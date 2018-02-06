/**
 * ===========
 * Cell action
 * ===========
 * 
 * This module defines the CellAction class,
 * along with it's methods and auxiliary definitions.
 */

#include <stdlib.h>

#include "cell_action.h"
#include "action_result.h"
#include "../../../utilities/random.h"



// ----- Main structure

// The structure is private and should not be accessed directly 
// from outside this file, but with the interface described in the 
// header file.  
struct CellAction_struct { /**
    
    Cell action.

    Class used to represent actions that the cell could perform.
    
    The object also holds the result of the computation, so that there
    is no need to constantly create new malloc'd structures.
    
    */
    Cell *cell;
    CellAction_fn *action;
    CellActionProb_fn *probability;
    ActionResult *result;
    
}; 

typedef struct CellAction_struct CellAction;



// ----- Methods

CellAction *CellAction_new(Cell *cell,
                           CellAction_fn *action_fn, 
                           CellActionProb_fn *probability_fn) { /**
    New cell action object.

    It is initialized with a function that when called will make
    the cell perform the action and a function that when called will
    calculate the probability to perform the action.

    */
    // Create
    CellAction *self = malloc(1 * sizeof(*self));
    // Initialize
    self->cell = cell;
    self->action = action_fn;
    self->probability = probability_fn;
    self->result = ActionResult_new();
    
    return self;
    
} // --- CellAction_new

CellAction *CellAction_del( CellAction *self ) { /**
    Deleter for an action object.
    */
    // Delete the result holder
    ActionResult_del(self->result);
    // Delete the action structure
    free(self);
}

ActionResult *CellAction_try_action( CellAction *self ) { /**
    Perform the action according to it's probability.
    */
    ActionResult *result = self->result;
    Cell *cell = self->cell;
    
    // Clear previous results information
    ActionResult_empty(result);
    
    if ( random_trial(self->probability(cell)) ){
        // Perform the action and save the result
        self->action(cell, result);
    }
    
    return result;
    
} // --- CellAction_try_action
