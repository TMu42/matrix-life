import os
import sys
import time

import life

import life.graphics as graph

import life.arguments as arg


ALGORITHMS = [life.numpy.roll,      #   7s / 100   @ 1300x280
              life.numpy.matmul,    # 200s / 100   @ 1300x280
              life.scipy.matmul,    #  11s / 100   @ 1300x280
              life.scipy.convolve]  #   8s / 100   @ 1300x280


sigmas = {5 : 10*[0] + [True],
          7 : 14*[0] + [True],
          8 : 16*[0] + [True],
          9 : 18*[0] + [True]}


def main(argv):
    world, surface, golife, frame, args = _initialize(argv)
    
    graph.paint_board(surface, world)
    
    try:
        while True:
            frame[-1] += 1
            
            graph.paint_board(surface, world)
            
            _wait(args.delay)
            
            if _update_sigmas(frame[-1], sum(sum(world))):
                world = golife.new_world(args.width, args.height)
                
                frame += [0]
                
                continue
            
            world = golife.step(world)
    except KeyboardInterrupt:
        pass


def _initialize(argv):
    args = arg.get_args(argv)
    
    surface = graph.initialize(args)
    
    golife = ALGORITHMS[args.algorithm]
    
    world = golife.new_world(args.width, args.height)
    
    frame = [0]
    
    return world, surface, golife, frame, args


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


def _get_kwargs(frame=None, count=None, sigmas=None, verbosity=0):
    if verbosity < 0:
        return {}
    elif verbosity == 0:
        return {"frame" : frame}
    elif verbosity == 1:
        return {"frame" : frame, "count" : count}
    else:
        return {"frame" : frame, "count" : count, "sigmas" : sigmas}


def _wait(seconds):
    if seconds < 0:
        input()
    else:
        time.sleep(seconds)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
