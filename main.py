import sys
import time
import pygame

import life.numpy.roll      #   7s / 100   @ 1300x280
import life.numpy.matmul    # 200s / 100   @ 1300x280
import life.scipy.matmul    #  11s / 100   @ 1300x280
import life.scipy.convolve  #   8s / 100   @ 1300x280

import life.terminal as term

import life.arguments as arg


ALGORITHMS = [life.numpy.roll,
              life.numpy.matmul,
              life.scipy.matmul,
              life.scipy.convolve]


sigmas = {5 : 10*[0] + [True],
          7 : 14*[0] + [True],
          8 : 16*[0] + [True],
          9 : 18*[0] + [True]}


def main(argv):
    args = arg.get_args(argv)
    
    golife = ALGORITHMS[args.algorithm]
    
    world, frame = golife.new_world(args.width, args.height), [0]
    
    term.prepare_terminal()
    
    term.print_board(world, **(_get_kwargs(frame, sigmas=sigmas,
                                           verbosity=args.verbose)))
    try:
        while True:
            frame[-1] += 1
            
            term.print_board(world, **(_get_kwargs(frame, sigmas=sigmas,
                                                   verbosity=args.verbose)))
            _wait(args.delay)
            
            if _update_sigmas(frame[-1], sum(sum(world))):
                world = golife.new_world(args.width, args.height)
                
                frame += [0]
                
                continue
            
            world = golife.step(world)
    except KeyboardInterrupt:
        print("\b\b  ", end='')
        
        sys.stdout.flush()
        
        term.end_terminal(world, **(_get_kwargs(frame, sigmas=sigmas,
                                                verbosity=args.verbose)))

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
