==========
CellSystem
==========

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
   :target: https://saythanks.io/inbox

An agent-based framework for the simulation of biological cell systems.

This was created to simulate cancer growth, taking into account nutrients and cell migration while allowing to track mutations, cell division and cell position history to study tumour phylogeny reconstruction algorithms.

.. image:: https://raw.githubusercontent.com/Ad115/Cell-System/master/assets/sidebyside.png
.. image:: https://raw.githubusercontent.com/Ad115/Cell-System/master/assets/spacetime.png


------------
Installation
------------

You can install it from PyPI::

    $ pip install cellsystem
    

-------
Example
-------

A use case integrated in the repository:

.. code-block:: python

    >>> from cellsystem import *

    # The cell system will simulate cell growth
    # while tracking the steps in that process.
    >>> system = CellSystem(grid_shape=(100, 100))

    # Initialize the first cell
    # in the middle of the grid
    >>> system.seed()
    
    
    New cell 0 added @ (50, 50)


    # Take 35 steps forward in time
    >>> system.run(steps=30)


    Cell no. 0 mutating @ site (50, 50) (father None)
             Initial mutations: []
                         Initial genome: AAAAAAAAAA
             Final mutations: [(4, 'G')]
                         Final genome: AAAAGAAAAA
    Cell no. 0 dividing @ (50, 50)
        New cells: 1 @ (49, 50) and 2 @ (50, 51)
    Cell no. 2 dividing @ (50, 51)
        New cells: 3 @ (51, 52) and 4 @ (51, 52)
    Cell no. 4 mutating @ site (51, 52) (father 2)
             Initial mutations: [(4, 'G')]
                         Initial genome: AAAAGAAAAA
             Final mutations: [(4, 'G'), (7, 'A')]
                         Final genome: AAAAGAAAAA
    Cell no. 1 death @ site (49, 50) (father None)
    Cell no. 3 death @ site (51, 52) (father 2)
    Cell no. 4 mutating @ site (51, 52) (father 2)
             Initial mutations: [(4, 'G'), (7, 'A')]
                         Initial genome: AAAAGAAAAA
             Final mutations: [(4, 'G'), (7, 'A'), (2, 'T')]
                         Final genome: AATAGAAAAA
    Cell no. 4 migrating from site (51, 52) (father 2)
         New site: (50, 52)
    ...
    ...
    ...


    # Prepare to explore the simulation logs
    >>> history = system['log']


    # First, let's see the cells' evolution in time and space!
    >>> history.worldlines().show()

    # Remove the cells that died somewhere along the way
    >>> history.worldlines(prune_death=True).show()
    

.. image:: https://raw.githubusercontent.com/Ad115/Cell-System/master/assets/geometry.png

.. image:: https://raw.githubusercontent.com/Ad115/Cell-System/master/assets/geometry_no_death.png


.. code-block:: python

    >>> tree_style = {'show_leaf_name' : True,
    ...               'mode' : 'c',        # Circular
    ...               'arc_start' : -135,  # Degrees
    ...               'arc_span' : 270 }   # Degrees also


    # Lookup the tree formed by cellular division
    >>> history.ancestry().show(styling=tree_style)

    # Now, remove cells that are no longer alive
    >>> history.ancestry(prune_death=True).show(styling=tree_style)


.. image:: https://raw.githubusercontent.com/Ad115/Cell-System/master/assets/ancestry.png

.. image:: https://raw.githubusercontent.com/Ad115/Cell-System/master/assets/ancestry_no_death.png


.. code-block:: python

    # Now, check out the tree formed by the mutations 
    >>> history.mutations().show(styling=tree_style)

    # Remove genomes with no living representatives.
    >>> history.mutations(prune_death=True).show(styling=tree_style)


.. image:: https://raw.githubusercontent.com/Ad115/Cell-System/master/assets/mutations.png

.. image:: https://raw.githubusercontent.com/Ad115/Cell-System/master/assets/mutations_no_death.png



*For more examples and usage, please refer to the [Wiki](wikigoeshere.com).*

----
Meta
----

**Author**: `Ad115 <https://agargar.wordpress.com/>`_ - `Github <https://github.com/Ad115/>`_ – a.garcia230395@gmail.com

Distributed under the MIT license. See `LICENSE <https://github.com/Ad115/Cell-System/blob/master/LICENSE>`_ for more information.

Warning: The project is still in alpha stage, so the API is just stabilizing and may change in the near future. This also means
that if you want to contribute, now is the right moment to make important change suggestions ;D

------------
Contributing
------------

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork `the repository <https://github.com/Ad115/Cell-System/>`_ on GitHub to start making your changes to a feature branch, derived from the **master** branch.
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and bug the maintainer until it gets merged and published. 
