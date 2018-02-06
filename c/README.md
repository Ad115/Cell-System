# C translation attempts

An attempt to translate to the C language the functionality in the `simplecells.py` script (written in Python).

The `simplecells.py` script is a simplified version of the whole simulation. It serves as a proof of concept. 

The `src/main.c` file is the entry point, equivalent to the main routine of the Python code.

The translation is done following the next guidelines:
 
 1. Each Python class is represented by a C struct.
> Example: The `CellLine` class corresponds to `struct CellLine`

 2. A class method is translated to a C global function with special naming as follows:
> Example: Calling `cell.new_daughter()` would translate to `Cell_new_daughter(cell)`, and
  `self.process()` would translate to `CellLine_process(self)`.

 3. The first argument of a class method should be the instance calling the method.
> Example: If `self` is an instance of the `CellAction` class, then `self.try_action(self.cell)` would translate to `CellAction_try_action(self, self->cell)`.

## How to run it

### The Python version

 1. Download the code. 
 2. Go to this folder (called `c`). 
 3. Execute in a terminal: `python3 simplecells.py`
 
Output:

```
Cell line: []

First cell: <index:0, father:None>

After division, cells are 2 (son of 0), and 1 (son of 0)

Now, let the system process every cell...
The cells in the system after that: [6, 3, 5, 4]
```

### The C equivalent

 1. Download the code. 
 2. Go to this folder (called `c`). 
 3. Type in a terminal: `make` to compile the code.
 4. Excecute the `main` binary that was created.
    
Output:

```
New cell line created: 
<CellLine object. Cells: []>

The first cell of the cell line: 
<Cell object. Index: 0, father: -1>

Now, the cell will take an action:
The cell has divided into: <Cell object. Index: 1, father: 0> and <Cell object. Index: 2, father: 0>

Now, let the system process every cell...
How is the system now?
<CellLine object. Cells: [4, 6, 3, 5, ]>
```
