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


// ----- Main structure

typedef struct CellLine_ CellLine /**
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
    */;



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
        
void CellLine_process( CellLine *self ) /**
    Move a step forward in time.
    */;
    
void CellLine_print( CellLine self ) /**
    Print the state of the cell line.
    */;
