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



// ----- Main structure
 
typedef struct Cell_ Cell /**
    
    A single cell.

    It acts according to it's state, and the states of nearby cells and sites.

    Attributes:
        + Index: A label that identifies it among others in the
                 same lineage.
        + Father: The index (lineage label) of it's father.
        + CellLine: The lineage this cell belongs to.
    */;



// ----- Methods
    
Cell *Cell_new( CellLine *lineage, int index ) /**
    Create a new cell.
    */;
    
void *Cell_del( Cell *self ) /**
    Deleter.
    */;

Cell *Cell_set_father( Cell *self, int father ) /**
    Initialize father.
    */;
    
Cell *Cell_set_index( Cell *self, int index ) /**
    Initialize index.
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
