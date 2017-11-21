Cell-System
-----------

Python classes for performing a simulation of cell growth, intended for cancer research.

The simulation is intended to be run in Processing.py (http://py.processing.org/tutorials/gettingstarted/). 

If you don't want a graphical output, all `*.py` files (except PSystem.py) are pure python scripts. To create a basic automaton,
you can type in the python console:

```python
>>> from cellsystem import System    # Import main class

>>> sys = System( gridDimensions=(10,10) )  # Create system of 10x10

>>> sys.seed()    # Place an initial cell
    # New cell added @ (50, 50)

>>> sys.step(10)    # Take 10 steps forward in time
    # Cell no. 0 migrating from site (5, 5) (father None)
    #        New site: (4, 4)
    # Cell no. 0 migrating from site (4, 4) (father None)
    #        New site: (3, 3)
    # Cell no. 0 migrating from site (3, 3) (father None)
    #       New site: (3, 4)
    # Cell no. 0 dividing @ (3, 4)
    #        New cells: 2 @ (4, 5) and 1 @ (2, 4)
    # Mutating cell no. 1 @ site (2, 4) (father None):
    #        Base genome: AAAAAAAAAA 
    #        Final mutations: [(2, 'C')]
    #        Final genome: AACAAAAAAA
    # Cell no. 1 dividing @ (2, 4)
    #        New cells: 4 @ (1, 3) and 3 @ (1, 3)
    # Cell no. 2 dying @ site (4, 5) (father 0)

>>> sys.totalCells()  # How many cells are alive now?
    # 2
```
