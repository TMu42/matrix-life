"""
A package containing implementations of Game of Life using NumPy.

This package contains modules specifying classes implementing the Model
component of a Model-View-Controller design pattern for Cellular Automata.
The Models provided herin implement Conway's Game of Life using data
structures and functions provided by NumPy.

Modules:
matmul  -- A module providing a Model object implementing Game of Life with
           standard matrix multiplication from NumPy.
roll    -- A module providing a Model object implementing Game of Life with
           the roll() function from NumPy.
"""

from . import roll
from . import matmul
