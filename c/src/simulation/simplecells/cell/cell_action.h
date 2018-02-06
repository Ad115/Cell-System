/**
 * ===========
 * Cell action
 * ===========
 * 
 * Header defining the external interface for the 
 * CellAction class, along with it's methods and 
 * auxiliary definitions.
 */
 
#pragma once

#include "../type_defs.h"



// Definition of CellAction_fn:
typedef ActionResult*(CellAction_fn)(Cell *, ActionResult *);

// Definition of CellActionProb_fn:
typedef float(CellActionProb_fn)(Cell *);



// ----- Methods

CellAction *CellAction_new(Cell *cell,
                           CellAction_fn *action_fn, 
                           CellActionProb_fn *probability_fn) /**
    New cell action object.

    It is initialized with a function that when called will make
    the cell perform the action and a function that when called will
    calculate the probability to perform the action.

    */;

CellAction *CellAction_del( CellAction *self ) /**
    Deleter for an action object.
    */;

ActionResult *CellAction_try_action( CellAction *self ) /**
    Perform the action according to it's probability.
    */;
