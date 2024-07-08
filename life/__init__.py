"""
A package containing implementations of Game of Life in Model-View-Controller.

This package contains a number of modules and subpackages specifying classes
implementing a version of the Model-View-Controller design pattern for
Cellular Automata. A number of Models, Views and Controllers are provided
chich can be used (relatively) interchangeably to assemble the desired device.

Modules:
arguments   -- A concreate module for command line argument handling for a
               main.py script. This module is due to be removed from the life
               package as it is inappropriately included.
terminal    -- A module providing View and Controller objects for a terminal
               based interface using curses.
graphics    -- A module providing View and Controller objects for a graphical
               interface using PyGame.
utils       -- A module providing functions of general utility. This module
               may be removed from the package at some point in the future as
               its value is not specific to this package.
mvc         -- A module providing Abstract Base Class descriptions for Model,
               View and Controller objects.

Subpackages:
nump        -- A package providing Model objects for Conway's Game of Life
               Cellular Automaton based on linear algebra provided by NumPy.
scip        -- A package providing Model objects for Conway's Game of Life
               Cellular Automaton based on linear algebra provided by SciPy.
"""

# Modules
from . import terminal
from . import graphics
from . import utils
from . import mvc

# Packages
from . import nump
from . import scip
