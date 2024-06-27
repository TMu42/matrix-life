import os
import sys
import time

import life

import life.terminal as term
import life.graphics as graph

import life.arguments as arg


#ALGORITHMS = [life.nump.roll,      #   7s / 100   @ 1300x280
#              life.nump.matmul,    # 200s / 100   @ 1300x280
#              life.scip.matmul,    #  11s / 100   @ 1300x280
#              life.scip.convolve]  #   8s / 100   @ 1300x280

ALGORITHMS = {arg.NP_ROLL[0]     : life.nump.roll,
              arg.NP_MATMUL[0]   : life.nump.matmul,
              arg.SP_MATMUL[0]   : life.scip.matmul,
              arg.SP_CONVOLVE[0] : life.scip.convolve}


sigmas = {5 : 10*[0] + [True],
          7 : 14*[0] + [True],
          8 : 16*[0] + [True],
          9 : 18*[0] + [True]}


def main(argv):
    global world, surface, golife, frame, args
    
    try:
        _initialize(argv)
        
        while _running():
            _paint_board(**(_kwargs(args.verbose)))
            
            _events()
            
            if not _paused():
                _wait(args.delay)
                
                if _update_sigmas(frame[-1], sum(sum(world))):
                    world = golife.new_world(*args.size)
                    
                    frame += [0]
                    
                    continue
                
                world = golife.step(world)
                
                frame[-1] += 1
            else:
                _wait(0.01)
    except KeyboardInterrupt:
        pass
    #except Exception as e:
    #    sys.stderr.write(str(e))
    
    _quit()


def _initialize(argv):
    global world, surface, golife, frame, args
    
    args = arg.get_args(argv)
    
    golife = ALGORITHMS[args.algorithm]
    
    world = golife.new_world(*args.size)
    
    frame = [0]
    
    if args.outmode in arg.TERMINAL:
        surface = term.initialize(args)
    elif args.outmode in arg.GRAPHICAL:
        surface = graph.initialize(args)


def _update_sigmas(frame, total):
    for key in sigmas:
        if sigmas[key][-1]:
            if total != sigmas[key][frame%(2*key)]:
                sigmas[key][frame%(2*key)] = total
                
                sigmas[key][-1] = False
            elif frame%(2*key) == 2*key - 1:
                return True
        else:
            sigmas[key][frame%(2*key)] = total
            
            if frame%(2*key) == 2*key - 1:
                sigmas[key][-1] = True
    
    return False


def _paint_board(**kwargs):
    if args.outmode in arg.GRAPHICAL:
        graph.paint_board(surface, world)
    elif args.outmode in arg.TERMINAL:
        term.paint_board(surface, world)#, **kwargs)


def _events():
    if args.outmode in arg.GRAPHICAL:
        graph.events()
    elif args.outmode in arg.TERMINAL:
        term.events()


def _running():
    global args
    
    if args.outmode in arg.GRAPHICAL:
        return graph.running
    elif args.outmode in arg.TERMINAL:
        return term.running
    else:
        return True


def _paused():
    if args.outmode in arg.GRAPHICAL:
        return graph.paused
    elif args.outmode in arg.TERMINAL:
        return term.paused
    else:
        return False


def _kwargs(verbosity=0):
    if verbosity < 0:
        return {}
    elif verbosity == 0:
        return {"frame" : frame}
    else:
        return {"frame" : frame, "count" : count, "sigmas" : sigmas}


def _wait(seconds):
    if seconds < 0:
        input()         ### BROKEN!!!!!
    else:
        time.sleep(seconds)


def _quit():
    if args.outmode in arg.GRAPHICAL:
        graph.end()
    elif args.outmode in arg.TERMINAL:
        term.end()
        #print("\b\b  ", end='')
        
        #sys.stdout.flush()
        
        #kwargs = _kwargs(args.verbose)
        
        #term.end_termianl(world, **kwargs)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
