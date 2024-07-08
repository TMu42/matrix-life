"""
A script to initialize and run Model-View-Controller based Cellular Automata.

Invoke with:
    
    python main.py [OPTIONS]

Options:
    -A, --algorithm=ALGORITHM
        Select the algorithm for executing Conway's Game of Life. ALGORITHM
        may be any of: "numpy-roll", "numpy-matmul", "scipy-matmul" or
        "scipy-convolve", or accepted aliases/abbreviations for these.
    
    -d, --delay=NUMBER
        Set the delay interval between iterations, 0 for no delay. NUMBER is
        in seconds but may take floating point values.
    
    -F, --fullscreen
        In graphical mode, set display to fullscreen.
    
    -O, --outmode=OUTMODE
        Select the output mode. OUTMODE may be either "terminal" or
        "graphical", or accepted aliases/abbreviations for these.
    
    -p, --paused (Ignored)
        Start Conway's Game of Life in paused mode. To toggle pause during
        execution, tap 'p'.
    
    -q, --quiet (Ignored)
        Decrease the verbosity of accompanying information to output for each
        instance of flag.
    
    -r, --resolution WIDTH [HEIGHT]
        Enter the display resolution for the output, if only WIDTH is
        specified, HEIGHT = WIDTH.
    
    -s, --size WIDTH [HEIGHT]
        Enter the size of the matrix to initialize for Conway's Game of Life.
        If only WIDTH is specified, HEIGHT = WIDTH.
    
    -v, --verbose (Ignored)
        Increase the verbosity of accompanying information to output for each
        instance of flag.
"""

import sys

import life

import arguments as arg


# Algorithm Analytics:
#
#   Tests on matrices of size 1300x280, values in seconds per 100 steps:
#       numpy roll:       7
#       scipy convolve:   8
#       scipy matmul:    11
#       numpy matmul:   200

MODELS = \
{
    **{key : life.nump.roll.GOLNumpyRollModel     for key in arg.DEFAULT},
    **{key : life.nump.roll.GOLNumpyRollModel     for key in arg.NP_ROLL},
    **{key : life.nump.matmul.GOLNumpyMatmulModel for key in arg.NP_MATMUL},
    **{key : life.scip.matmul.GOLScipyMatmulModel for key in arg.SP_MATMUL},
    **{key : life.scip.convolve.GOLScipyConvolveModel
                                                  for key in arg.SP_CONVOLVE}
}

VIEWS = \
{
    **{key : life.graphics.GraphicsView for key in arg.DEFAULT},
    **{key : life.graphics.GraphicsView for key in arg.GRAPHICAL},
    **{key : life.terminal.TerminalView for key in arg.TERMINAL}
}

CONTROLLERS = \
{
    **{key : life.graphics.GraphicsController for key in arg.DEFAULT},
    **{key : life.graphics.GraphicsController for key in arg.GRAPHICAL},
    **{key : life.terminal.TerminalController for key in arg.TERMINAL}
}


def main(argv):
    controller = _initialize(argv)
    
    controller.run()
    
    return 0


def _initialize(argv):
    args = arg.get_args(argv)
    
    model = MODELS[args.algorithm](args.size)
    
    view = VIEWS[args.outmode](resolution=args.resolution,
                               fullscreen=args.fullscreen)
    
    controller = CONTROLLERS[args.outmode](model, view, args.delay,
                                                        args.paused)
    
    return controller


if __name__ == "__main__":
    sys.exit(main(sys.argv))
