/**
 * ===================
 * Cell action result
 * ===================
 * 
 * Header defining the external interface for the
 * ActionResult class, along with methods and auxiliary 
 * definitions.
 */
 
#pragma once



// ----- Main structure

typedef struct AResult_ ActionResult /*
    
    Cell action result.

    Represents the result of a computation on a biological entity.
    */;



// ----- Methods

ActionResult *ActionResult_new() /**
    New cell action result object.

    It is initialized with a function that when called will make
    the cell perform the action and a function that when called will
    calculate the probability to perform the action.
    */;

void ActionResult_del( ActionResult *self ) /**
    Deleter for an action object.
    */;

ActionResult *ActionResult_add_cell( ActionResult *self, Cell *cell ) /**
    Perform the action according to it's probability.
    */;

Cell *ActionResult_pop_cell( ActionResult *self ) /**
    Remove the last cell and return it.
    */;

ActionResult *ActionResult_empty( ActionResult *self ) /**
    Clear the state of the structure.
    */;
