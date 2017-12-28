"""The biological entities.

Every cell belongs to a cell line.

The cell line is in charge of:
    - creating and initializing new cells
    - managing the disposal of dead cells
    - manage the ancestral genome of the descendants.
    
A cell can perform actions like:
    - migrate, 
    - mutate,
    - divide,
    - die.

"""

from .lineage import CellLine

__all__ = ['CellLine']