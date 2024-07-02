import os
import sys
import time

import life

#import life.nump.roll     as nproll
#import life.nump.matmul   as npmatmul
#import life.scip.matmul   as spmatmul
#import life.scip.convolve as spconv

import life.terminal as term
import life.graphics as graph

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
    
    #if args.algorithm in arg.DEFAULT:
    #    args.algorithm = arg.NP_ROLL[0]
    #
    #if args.algorithm in arg.NP_ROLL:
    #    model = nproll.GOLNumpyRollModel(args.size)
    #elif args.algorithm in arg.NP_MATMUL:
    #    model = npmatmul.GOLNumpyMatmulModel(args.size)
    #elif args.algorithm in arg.SP_MATMUL:
    #    model = spmatmul.GOLScipyMatmulModel(args.size)
    #elif args.algorithm in arg.SP_CONVOLVE:
    #    model = spconv.GOLScipyConvolveModel(args.size)
    
    if args.outmode in arg.DEFAULT:
        args.outmode = arg.TERMINAL[0]
    
    if args.outmode in arg.TERMINAL:
        view = term.TerminalView(resolution=args.resolution,
                                 fullscreen=args.fullscreen)
        
        controller = term.TerminalController(model)
    elif args.outmode in arg.GRAPHICAL:
        view = graph.GraphicsView(resolution=args.resolution,
                                  fullscreen=args.fullscreen)
        
        controller = graph.GraphicsController(model, view, args.delay)
    
    return controller


#def _update_sigmas(frame, total):
#    for key in sigmas:
#        if sigmas[key][-1]:
#            if total != sigmas[key][frame%(2*key)]:
#                sigmas[key][frame%(2*key)] = total
#                
#                sigmas[key][-1] = False
#            elif frame%(2*key) == 2*key - 1:
#                return True
#        else:
#            sigmas[key][frame%(2*key)] = total
#            
#            if frame%(2*key) == 2*key - 1:
#                sigmas[key][-1] = True
#    
#    return False


#def _paint_board(**kwargs):
#    if args.outmode in arg.GRAPHICAL:
#        graph.paint_board(surface, world)
#    elif args.outmode in arg.TERMINAL:
#        term.paint_board(surface, world)#, **kwargs)


#def _events():
#    if args.outmode in arg.GRAPHICAL:
#        graph.events()
#    elif args.outmode in arg.TERMINAL:
#        term.events()


#def _running():
#    global args
#    
#    if args.outmode in arg.GRAPHICAL:
#        return graph.running
#    elif args.outmode in arg.TERMINAL:
#        return term.running
#    else:
#        return True


#def _paused():
#    if args.outmode in arg.GRAPHICAL:
#        return graph.paused
#    elif args.outmode in arg.TERMINAL:
#        return term.paused
#    else:
#        return False


#def _kwargs(verbosity=0):
#    if verbosity < 0:
#        return {}
#    elif verbosity == 0:
#        return {"frame" : frame}
#    else:
#        return {"frame" : frame, "count" : count, "sigmas" : sigmas}


#def _wait(seconds):
#    if seconds < 0:
#        input()         ### BROKEN!!!!!
#    else:
#        time.sleep(seconds)


#def _quit():
#    pass
    #if args.outmode in arg.GRAPHICAL:
    #    graph.end()
    #elif args.outmode in arg.TERMINAL:
    #    term.end()
        #print("\b\b  ", end='')
        
        #sys.stdout.flush()
        
        #kwargs = _kwargs(args.verbose)
        
        #term.end_termianl(world, **kwargs)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
