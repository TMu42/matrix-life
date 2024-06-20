import sys
import time

#import life.numpy.roll as life      #   7s / 100   @ 1300x280
#import life.numpy.matmul as life    # 200s / 100   @ 1300x280
#import life.scipy.matmul as life    #  11s / 100   @ 1300x280
import life.scipy.convolve as life  #   8s / 100   @ 1300x280

import life.terminal as term


WIDTH  = 130
HEIGHT =  28

PRINT_WIDTH  = 130
PRINT_HEIGHT =  28

DELAY = 0.05

#COUNT_END = 50
    
sigmas = {5 : 10*[0] + [True],
          7 : 14*[0] + [True],
          8 : 16*[0] + [True],
          9 : 18*[0] + [True]}


def main(argv):
    world = life.new_world(WIDTH, HEIGHT)
    
    sigma, count = sum(sum(world)), 0
    
    frame = [0]
    
    term.prepare_terminal()
    
    term.print_board(world, frame, count, sigmas)
    
    try:
        while True:
            frame[-1] += 1
            
            term.print_board(world, frame, count, sigmas)
            
            time.sleep(DELAY)
            #input()
            
            if update_sigmas(frame[-1], sum(sum(world))):
                world, count = life.new_world(WIDTH, HEIGHT), 0
                
                frame += [0]
                
                continue
            
            if sum(sum(world)) == sigma:
                count += 1
            else:
                sigma, count = sum(sum(world)), 0
            
            #if count == COUNT_END:
            #    world, count = life.new_world(WIDTH, HEIGHT), 0
            #    
            #    frame += [0]
            #    
            #    continue
            
            world = life.step(world)
    except KeyboardInterrupt:
        print("\b\b  ", end='')
        
        sys.stdout.flush()
        
        term.end_terminal(world, frame, count, sigmas)


def update_sigmas(frame, total):
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


if __name__ == "__main__":
    sys.exit(main(sys.argv))
