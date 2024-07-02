import os
import sys
import time

import life

#import life.terminal as term
#import life.graphics as graph

import life.arguments as arg


# Algorithm Analytics:
#
#   Tests on matrices of size 1300x280, valuse in seconds per 100 steps:
#       numpy roll:       7
#       scipy convolve:   8
#       scipy matmul:    11
#       numpy matmul:   200

MODELS = {**{key : life.nump.roll.GOLNumpyRollModel for key in arg.DEFAULT},
          **{key : life.nump.roll.GOLNumpyRollModel for key in arg.NP_ROLL},
          **{key : life.nump.matmul.GOLNumpyMatmulModel
                                                    for key in arg.NP_MATMUL},
          **{key : life.scip.matmul.GOLScipyMatmulModel
                                                    for key in arg.SP_MATMUL},
          **{key : life.scip.convolve.GOLScipyConvolveModel
                                                    for key in arg.SP_CONVOLVE}
         }

VIEWS = {**{key : life.graphics.GraphicsView for key in arg.DEFAULT},
         **{key : life.graphics.GraphicsView for key in arg.GRAPHICAL},
         **{key : life.terminal.TerminalView for key in arg.TERMINAL}
        }

CONTROLLERS = {**{key : life.graphics.GraphicsController
                                                for key in arg.DEFAULT},
               **{key : life.graphics.GraphicsController
                                                for key in arg.GRAPHICAL},
               **{key : life.terminal.TerminalController
                                                for key in arg.TERMINAL}
              }


#sigmas = {5 : 10*[0] + [True],
#          7 : 14*[0] + [True],
#          8 : 16*[0] + [True],
#          9 : 18*[0] + [True]}


def main(argv):
    controller = _initialize(argv)
    
    controller.run()
    
    return 0


def _initialize(argv):
    args = arg.get_args(argv)
    
    model = MODELS[args.algorithm](args.size)
    
    #if args.outmode in arg.DEFAULT:
    #    args.outmode = arg.TERMINAL[0]
    
    view = VIEWS[args.outmode](resolution=args.resolution,
                               fullscreen=args.fullscreen)
    
    controller = CONTROLLERS[args.outmode](model, view, args.delay)
    
    #if args.outmode in arg.TERMINAL:
    #    view = term.TerminalView(resolution=args.resolution,
    #                             fullscreen=args.fullscreen)
    #    
    #    controller = term.TerminalController(model, view, args.delay)
    #elif args.outmode in arg.GRAPHICAL:
    #    view = graph.GraphicsView(resolution=args.resolution,
    #                              fullscreen=args.fullscreen)
    #    
    #    controller = graph.GraphicsController(model, view, args.delay)
    
    return controller


if __name__ == "__main__":
    sys.exit(main(sys.argv))
