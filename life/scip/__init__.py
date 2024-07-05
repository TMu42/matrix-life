"""
A package containing implementations of Game of Life using SciPy with NumPy.

This package contains modules specifying classes implementing the Model
component of a Model-View-Controller design pattern for Cellular Automata.
The Models provided herin implement Conway's Game of Life using data
structures provided by NumPy and SciPy and functions provided by SciPy.

Modules:
matmul      -- A module providing a Model object implementing Game of Life
               with sparse matrix multiplication from SciPy.
convolve    -- A module providing a Model object implementing Game of Life
               with the ndimage.convolve() function from SciPy.
"""

from . import matmul
from . import convolve
