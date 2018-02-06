/**
 * ====
 * Cell
 * ====
 * 
 * Implementation file for the Cell class, along 
 * with methods and auxiliary definitions.
 */

#include <stdlib.h>
#include <stdio.h>

#include "cell.h"
#include "cell_action.h"
#include "action_result.h"
#include "../cell_line.h"
#include "../../../utilities/list.h"
#include "../../../utilities/random.h"

#define NO_FATHER (-1)


// ----- Main structure

// The structure is private and should not be accessed directly 
// from outside this file, but with the interface described in the 
// header file.  
struct Cell_struct { /**
    
    A single cell.

    It acts according to it's state, and the states of nearby cells and sites.

    Attributes:
        + Index: A label that identifies it among others in the
                 same lineage.
        + Father: The index (lineage label) of it's father.
        + CellLine: The lineage this cell belongs to.
    */
    int index;
    int father;
    CellLine *lineage;
    List *actions;
    
};

typedef struct Cell_struct Cell;


// ----- Methods

Cell *Cell_new( CellLine *lineage, int index ) { /**
        + Index: A label that identifies it among others in the
                 same lineage.
        + CellLine: The lineage this cell belongs to.
    */
    // Create
    Cell *self = malloc(1 * sizeof(*self));
    // Initialize
    self->index = index;
    self->lineage = lineage;
    self->father = NO_FATHER;
    self->actions = Cell_init_actions(self);
    
    return self;
    
} // --- Cell_new

void Cell_del_actions( Cell *self ) { /**
    Deleter for the actions list.
    */
    List *actions = self->actions;
    
    // First remove the actions in the list
    for(int i=0; i < List_size(actions); i++) {
        // Fetch the ith action
        CellAction *item = List_at(actions, i);
        // Remove the action
        CellAction_del(item);
    }
    
    // Remove the list
    List_del(self->actions);
    
} // --- Cell_del_actions
    
void *Cell_del( Cell *self ) { /**
    Deleter.
    */
    Cell_del_actions(self);
    free(self);
    
} // --- Cell_del

Cell *Cell_set_father( Cell *self, int father ) { /**
    Initialize father.
    */
    self->father = father;
    
    return self;

} // --- Cell_set_father

int Cell_index( Cell *self ) { /**
    Getter for the cell index.
    */
    return self->index;
    
} // --- Cell_index

Cell *Cell_set_index( Cell *self, int index ) { /**
    Initialize index.
    */
    self->index = index;
    
    return self;

} // --- Cell_set_index

ActionResult *Cell_divide( Cell *self, ActionResult *result ) { /**
    
    Cell division.

    Two new cells are created from a single parent.
    */
    
    // Create the daughter cell
    Cell *daughter = Cell_new_daughter(self);

    // We want both resulting cells to be daughters of the
    // father cell.
    int father = self->index;
    CellLine_recycle_cell(self->lineage, self, father);
    
    // The result consists of both cells
    ActionResult_add_cell(result, self);
    ActionResult_add_cell(result, daughter);
    return result;
    
} // --- Cell_divide

float Cell_division_probability( Cell *self ) { /**
    Probability that this cell will divide if selected for division.
    */
    return 1.;
    
} // --- Cell_division_probability

Cell *Cell_new_daughter( Cell *self ) { /**
    Initialize a new daughter cell.

    Initialize with father and mutation attributes.
    
    */
    int father = self->index;
    
    Cell *daughter = CellLine_new_cell(self->lineage);
    Cell_set_father(daughter, father);
    
    return daughter;
    
} // --- Cell_new_daughter

List *Cell_init_actions( Cell *self ) { /**
    Return a list with the possible actions to take for this cell.
    */
    // Create each individual action
    CellAction *division = CellAction_new(self, 
                                          &Cell_divide, 
                                          &Cell_division_probability);
    // Create the actions array
    List *actions = List_new();
    // Fill it
    List_push(actions, division);
    
    return actions;
    
} // --- Cell_init_actions

ActionResult *Cell_process( Cell *self ) { /**
    Select an action and perform it.
    */
    // Select an action
    CellAction *action = List_random_item(self->actions);
        
    // Perform the action according to it's respective probability
    return CellAction_try_action(action);
    
} // --- Cell_process

void Cell_print( Cell *self ) { /**
    Print the state of the cell.
    */
    printf("<Cell object. Index: %d, father: %d>", self->index, self->father);
    
} // --- Cell_print
