/**
 * =========
 * Cell line
 * =========
 * 
 * Header defining the external interface for the 
 * CellLine class, along with methods and auxiliary 
 * definitions.
 */
 
#pragma once

// Include the header defining the types.
#include "type_defs.h"


// ----- Methods

CellLine *CellLine_new( ) /**
        Creation of a cell lineage.
        */;

void CellLine_del( CellLine *self ) /**
    Deleter for a cell line object.
    */;

Cell *CellLine_new_cell( CellLine *self) /**
    Get a new blank cell in this lineage and system.
    */;
    
Cell *CellLine_recycle_cell(CellLine *self, 
                            Cell *cell, 
                            int father) /**
    Clear previous information from a cell.
    */;
        
CellLine *CellLine_process( CellLine *self ) /**
    Move a step forward in time.
    */;
    
void CellLine_print( CellLine *self ) /**
    Print the state of the cell line.
    */;
