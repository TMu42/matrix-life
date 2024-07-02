import os
import sys
import time

import life

import life.arguments as arg


# Algorithm Analytics:
#
#   Tests on matrices of size 1300x280, valuse in seconds per 100 steps:
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
    
    controller = CONTROLLERS[args.outmode](model, view, args.delay)
    
    return controller


if __name__ == "__main__":
    sys.exit(main(sys.argv))
