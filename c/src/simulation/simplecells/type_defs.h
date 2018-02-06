/**
 * =================================
 * Cell related classes definitions
 * =================================
 * 
 * Header defining the structures representing 
 * biological agents.
 * The methods related to each class are defined in their
 * respective header.
 * 
 * Classes defined here:
 *      + CellLine
 *      + Cell
 *          - CellAction
 *          - ActionResult
 */
 
#pragma once



/* ------- Main structures -------- */
    
typedef struct CellLine_struct CellLine /**
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
 

typedef struct Cell_struct Cell /**
    
    A single cell.

    It acts according to it's state, and the states of nearby cells and sites.

    Attributes:
        + Index: A label that identifies it among others in the
                 same lineage.
        + Father: The index (lineage label) of it's father.
        + CellLine: The lineage this cell belongs to.
    */;


typedef struct CellAction_struct CellAction /**
    
    Cell action.

    Class used to represent actions that the cell could perform.
    */; 
    
    
typedef struct ActionResult_struct ActionResult /*
    
    Cell action result.

    Represents the result of a computation on a biological entity.
    */;

