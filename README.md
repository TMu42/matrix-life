# Matrix Life (matrix-life)
Conway's Game of Life using Matrices implemented in Python.

## Summary

This repository implements the classic [Cellular Automaton](https://en.wikipedia.org/wiki/Cellular_automaton) [John Conway](https://en.wikipedia.org/wiki/John_Horton_Conway)'s [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in Python, using NumPy Matrices and various [Linear Algebra](https://en.wikipedia.org/wiki/Linear_algebra) functions from NumPy and SciPy. Output is either terminal based or graphical with parameters selectable at invocation or during execution.

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

                                 -p, --paused
                                         Start Conway's Game of Life in paused mode. To
                                         toggle pause during execution, tap 'p'.

                                 -q, --quiet
                                         Decrease the verbosity of accompanying information
                                         to output for each instance of flag.

                                 -r, --resolution WIDTH [HEIGHT]
                                         Enter the display resolution for the output, if
                                         only WIDTH is specified, HEIGHT = WIDTH.

                                 -s, --size WIDTH [HEIGHT]
                                         Enter the size of the matrix to initialize for
                                         Conway's Game of Life. If only WIDTH is specified,
                                         HEIGHT = WIDTH.

                                 -v, --verbose
                                         Increase the verbosity of accompanying information
                                         to output for each instance of flag.

    
    gmain.py            -    Graphical version of main python script, (deprecated, use main.py).
                             Invoke with:
                             
                                 python gmain.py [OPTIONS]
                             
                             Options: see main.py
    
    tmain.py            -    Terminal version of main python script, (deprecated, use main.py).
                             Invoke with:
                             
                                 python tmain.py [OPTIONS]
                             
                             Options: see main.py
    
    icon.ico            -    Favicon style icon file for graphics mode window.
    
    requirements.txt    -    Dependency list for this repository, install into virtual environment
                             or globally with:
                             
                                 pip install -r requirements.txt
    
    README.md           -    This README file

### matrix-life/life/
    
    __init__.py     -    Initiation file for package life
    
    arguments.py    -    CLI argument handling with argparse
    
    graphics.py     -    Graphical output handling with PyGame
    
    terminal.py     -    Terminal output handling

    utils.py        -    Shared general utility functions

### matrix-life/life/nump/
    
    __init__.py    -    Initiation file for subpackage numpy
    
    roll.py        -    Game of Life implementation with numpy.roll()
    
    matmul.py      -    Game of Life implementation with numpy.ndarray.__matmul__()

### matrix-life/life/scip/
    
    __init__.py    -    Initiation file for subpackage scipy
    
    convolve.py    -    Game of Life implementation with scipy.ndimage.convolve()
    
    matmul.py      -    Game of Life implementation with scipy.sparse.__matmul__()
