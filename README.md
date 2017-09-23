Cell-System
-----------

Python classes for performing a simulation of cell growth, intended for cancer research.

The simulation is intended to be run in Processing.py (http://py.processing.org/tutorials/gettingstarted/). 

If you don't want a graphical output, all `*.py` files (except PSystem.py) are pure python scripts. To create a basic automaton,
you can type in the python console:

```
>>> from cellSystem.system import System    # Import main class

>>> system = System( gridDimensions=(10,10) )  # Create an empty system

>>> system.seed()    # Place an initial cell

>>> for _ in range(10): system.step()    # Take 10 steps forward in time

>>> system.totalAliveCells()  # How many cells are now?
```
