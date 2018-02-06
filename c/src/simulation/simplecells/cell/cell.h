/**
 * ====
 * Cell
 * ====
 * 
 * Header defining the external interface for the 
 * Cell class, along with it's methods and 
 * auxiliary definitions.
 */
 
#pragma once

#include "../../../utilities/list.h"
#include "../type_defs.h"



// ----- Methods
    
Cell *Cell_new( CellLine *lineage, int index ) /**
    Create a new cell.
    */;
    
void *Cell_del( Cell *self ) /**
    Deleter.
    */;

Cell *Cell_set_father( Cell *self, int father ) /**
    Setter for cell father.
    */;

int Cell_index( Cell *self ) /**
    Getter for cell index.
    */;
    
Cell *Cell_set_index( Cell *self, int index ) /**
    Setter for cell index.
    */;

ActionResult *Cell_divide( Cell *self, ActionResult *result ) /**
    Cell division.

    Two new cells are created from a single parent.
    */;

float Cell_division_probability( Cell *self ) /**
    Probability that this cell will divide if selected for division.
    */;

Cell *Cell_new_daughter( Cell *self ) /**
    Initialize a new daughter cell.
    */;

List *Cell_init_actions( Cell *self ) /**
    Return a list with the possible actions to take for this cell.
    */;
    
void Cell_del_actions( Cell *self ) /**
    Deleter for the actions list.
    */;

ActionResult *Cell_process( Cell *self ) /**
    Select an action and perform it.
    */;

void Cell_print( Cell *self ) /**
    Print the state of the cell.
    */;
