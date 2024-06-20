import sys
import time

#import life.numpy.roll as life      #   7s / 100   @ 1300x280
#import life.numpy.matmul as life    # 200s / 100   @ 1300x280
#import life.scipy.matmul as life    #  11s / 100   @ 1300x280
import life.scipy.convolve as life  #   8s / 100   @ 1300x280

import life.terminal as term


WIDTH  = 1300
HEIGHT =  280

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
    
    term.print_board(world, frame, count)
    
    try:
        while True:
            frame[-1] += 1
            
            term.print_board(world, frame, count)
            
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
        #cursor_to(HEIGHT + 4, 0)
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


#def print_board(mat, frame=None, count=None, cls=True):
#    if cls:
#        cursor_to(1, 0)
#    
#    print(' +' + min(len(mat[0]), PRINT_WIDTH)*'=' + '+')
#    
#    for row in mat[:PRINT_HEIGHT]:
#        print(' |', end='')
#        
#        for c in row[:PRINT_WIDTH]:
#            print('#' if c else ' ', end='')
#            #print(c, end='')
#        
#        print('|')
#    
#    print(' +' + min(len(mat[0]), PRINT_WIDTH)*'=' + '+')
#    
#    for key in sigmas:
#        print(f"{key}: {sigmas[key]}  ")
#    
#    if frame is not None:
#        f = frame[-10:]
#        
#        if len(f) < len(frame):
#            f = ['...'] + f
#        
#        print(f"Frame: {sum(frame)} {f[::-1]}    ", end='')
#    
#    if count is not None:
#        print(f"Count: {count}    ", end='')


def cursor_to(y, x):
    print(f"\033[{y};{x}H")

if __name__ == "__main__":
    sys.exit(main(sys.argv))
