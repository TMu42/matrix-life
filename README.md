# Matrix Life (matrix-life)
Conway's Game of Life using Matrices implemented in Python.

## Summary

This repository implements the classic [Cellular Automaton](https://en.wikipedia.org/wiki/Cellular_automaton) [John Conway](https://en.wikipedia.org/wiki/John_Horton_Conway)'s [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in Python, using NumPy Matrices and various [Linear Algebra](https://en.wikipedia.org/wiki/Linear_algebra) functions from NumPy and SciPy.

## Files
### matrix-life/
    
    main.py             -    Main python script to execute versions of Conway's Game of Life
                             
                             Options:
                                 -W, --width=NUMBER
                                         Set the width (number of columns) of the cellular automaton, 0 to infer from
                                         the terminal.
                                   
                                 -H, --height=NUMBER
                                         Set the height (number of rows/lines) of the cellular automaton, 0 to infer
                                         from the terminal.

                                 -D, --delay=NUMBER
                                         Set the delay interval between iterations, 0 for no delay, negative for user
                                         step-by-step mode.

                                 -R, --numpy-roll
                                         Select the numpy.roll() implementation of the Game of Life algorithm.

                                 -M, --numpy-matmul
                                         Select the numpy.ndarray.__matmul__() implementation of the Game of Life
                                         algorithm.

                                 -S, --scipy-matmul
                                         Select scipy.sparse.__matmul__() implementation of the Game of Life
                                         algorithm.

                                 -C, --scipy-convolve
                                         Select scipy.ndimage.__convolve__() implementation of the Game of Life
                                         algorithm.
    
    requirements.txt    -    Dependency list for this repository, install into virtual environment or globally with:
                             
                                 pip install -r requirements.txt

### matrix-life/life/
    
    __init__.py     -    Initiation file for package life
    
    arguments.py    -    CLI argument handling with argparse
    
    terminal.py     -    Terminal output handling

### matrix-life/life/numpy/
    
    __init__.py    -    Initiation file for subpackage numpy
    
    roll.py        -    Game of Life implementation with numpy.roll()
    
    matmul.py      -    Game of Life implementation with numpy.ndarray.__matmul__()

### matrix-life/life/scipy/
    
    __init__.py    -    Initiation file for subpackage scipy
    
    convolve.py    -    Game of Life implementation with scipy.ndimage.convolve()
    
    matmul.py      -    Game of Life implementation with scipy.sparse.__matmul__()
