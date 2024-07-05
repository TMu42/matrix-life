# Matrix Life (matrix-life)
Conway's Game of Life using Matrices implemented in Python.

## Summary

This repository implements a [Linear Algebra](https://en.wikipedia.org/wiki/Linear_algebra) model of the classic [Cellular Automaton](https://en.wikipedia.org/wiki/Cellular_automaton) [John Conway](https://en.wikipedia.org/wiki/John_Horton_Conway)'s [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in Python, using a variant of the [Model-View-Controller](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) design pattern. Different Model classes are provided to implement the algorithm using various [Linear Algebra](https://en.wikipedia.org/wiki/Linear_algebra) functions from NumPy and SciPy. View-Controller class pairs are provided to output either to the terminal (with curses) or to a graphical interface (with PyGame). These can be selected from the command line via options/arguments to the `main.py` script or alternatively the modules can be imported and assembled interactively from the python interpreter.

## Files
### matrix-life/
    
    main.py             -    Main python script to execute versions of Conway's Game of Life. 
                             Invoke with:
                             
                                 python main.py [OPTIONS]
                             
                             Options:
                                 -A, --algorithm=ALGORITHM
                                         Select the algorithm for executing Conway's Game of
                                         Life. ALGORITHM may be any of: "numpy-roll",
                                         "numpy-matmul", "scipy-matmul" or "scipy-convolve",
                                         or accepted aliases/abbreviations for these.
                                 
                                 -d, --delay=NUMBER
                                         Set the delay interval between iterations, 0 for no
                                         delay. NUMBER is in seconds but may take floating
                                         point values.
                                 
                                 -F, --fullscreen
                                         In graphical mode, set display to fullscreen.

                                 -O, --outmode=OUTMODE
                                         Select the output mode. OUTMODE may be either
                                         "terminal" or "graphical", or accepted aliases/
                                         abbreviations for these.

                                 -p, --paused (Ignored)
                                         Start Conway's Game of Life in paused mode. To
                                         toggle pause during execution, tap 'p'.

                                 -q, --quiet (Ignored)
                                         Decrease the verbosity of accompanying information
                                         to output for each instance of flag.

                                 -r, --resolution WIDTH [HEIGHT]
                                         Enter the display resolution for the output, if
                                         only WIDTH is specified, HEIGHT = WIDTH.

                                 -s, --size WIDTH [HEIGHT]
                                         Enter the size of the matrix to initialize for
                                         Conway's Game of Life. If only WIDTH is specified,
                                         HEIGHT = WIDTH.

                                 -v, --verbose (Ignored)
                                         Increase the verbosity of accompanying information
                                         to output for each instance of flag.
    
    icon.ico            -    Favicon style icon file for graphics mode window.
    
    requirements.txt    -    Dependency list for this repository, install into virtual environment
                             or globally with:
                             
                                 pip install -r requirements.txt
    
    README.md           -    This README file

### matrix-life/life/
    
    __init__.py     -    Initiation file for package life
    
    arguments.py    -    CLI argument handling with argparse
    
    graphics.py     -    View and Controller classes for graphical output handling with PyGame

    mvc.py          -    Abstract Base Class descriptions for Model-View-Controller objects
    
    terminal.py     -    View and Controller classes for terminal output handling with curses

    utils.py        -    Shared general utility functions

### matrix-life/life/nump/
    
    __init__.py    -    Initiation file for subpackage numpy
    
    roll.py        -    Model class for Game of Life implementation with numpy.roll()
    
    matmul.py      -    Model class for Game of Life implementation with numpy.ndarray.__matmul__()

### matrix-life/life/scip/
    
    __init__.py    -    Initiation file for subpackage scipy
    
    convolve.py    -    Model class for Game of Life implementation with scipy.ndimage.convolve()
    
    matmul.py      -    Model class for Game of Life implementation with scipy.sparse.__matmul__()
