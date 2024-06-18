import sys
import time

import numpy as np


WIDTH  = 1280
HEIGHT =  720

PRINT_WIDTH  = 130
PRINT_HEIGHT =  28

DELAY = 0.004

COUNT_END = 50

ONE = np.uint8(1)
ZRO = np.uint8(0)


def main(argv):
    rng = np.random.default_rng()
    
    world = rng.integers(2, size=[HEIGHT, WIDTH], dtype=np.uint8)
    
    sigma = sum(sum(world))
    count = 0
    
    print_board(world[:PRINT_HEIGHT, :PRINT_WIDTH], cls=False)
    
    try:
        while True:
            print_board(world[:PRINT_HEIGHT, :PRINT_WIDTH])
            
            time.sleep(DELAY)
            #input()
            
            if sum(sum(world)) == sigma:
                count += 1
            else:
                sigma = sum(sum(world))
                
                count = 0
            if count == COUNT_END:
                world = rng.integers(2, size=[HEIGHT, WIDTH], dtype=np.uint8)
                
                continue
            
            #world = life_step_matmul(world)
            world = life_step_roll(world)
    except KeyboardInterrupt:
        cursor_to(HEIGHT + 3, 0)


L = np.roll(np.identity(WIDTH,  dtype=np.uint8), shift=1,  axis=1)
R = np.roll(np.identity(WIDTH,  dtype=np.uint8), shift=-1, axis=1)
U = np.roll(np.identity(HEIGHT, dtype=np.uint8), shift=1,  axis=0)
D = np.roll(np.identity(HEIGHT, dtype=np.uint8), shift=-1, axis=0)

def life_step_matmul(A):
    up_down = (U + D)@A
    lr_corn = (A + (U + D)@A)@(L + R)
    
    neighbours = up_down + lr_corn
    
    generate = np.minimum(neighbours//3, 1) - np.minimum(neighbours//4, 1)
    
    survive = (np.minimum(neighbours//2, 1) - np.minimum(neighbours//4, 1))
    
    return np.maximum(generate, A*survive)
    
    #itrA = np.nditer(A)
    #itrN = np.nditer(neighbours)
    
    #return np.array([ONE if (a == 1 and n > 1 and n < 4) or n == 3 else ZRO \
    #                           for a, n in zip(itrA, itrN)]).reshape(A.shape)


def life_step_roll(A):
    neighbours = np.roll(A, ( 1,  0), (0, 1)) \
               + np.roll(A, (-1,  0), (0, 1)) \
               + np.roll(A, ( 0,  1), (0, 1)) \
               + np.roll(A, ( 0, -1), (0, 1)) \
               + np.roll(A, ( 1,  1), (0, 1)) \
               + np.roll(A, ( 1, -1), (0, 1)) \
               + np.roll(A, (-1,  1), (0, 1)) \
               + np.roll(A, (-1, -1), (0, 1)) \
    
    #generate = (2*neighbours)%5%4%3%2
    
    #survive = A*(4*neighbours)%7%6%5%4%3%2
    
    generate = np.minimum(neighbours//3, 1) - np.minimum(neighbours//4, 1)
    
    survive = (np.minimum(neighbours//2, 1) - np.minimum(neighbours//4, 1))
    
    return np.maximum(generate, A*survive)
    
    #itrA = np.nditer(A)
    #itrN = np.nditer(neighbours)
    
    #return np.array([ONE if (a == 1 and n > 1 and n < 4) or n == 3 else ZRO \
    #                           for a, n in zip(itrA, itrN)]).reshape(A.shape)


def print_board(mat, cls=True):
    if cls:
        cursor_to(1, 0)
    
    print(' +' + len(mat[0])*'=' + '+')
    
    for row in mat:
        print(' |', end='')
        
        for c in row:
            print('#' if c else ' ', end='')
            #print(c, end='')
        
        print('|')
    
    print(' +' + len(mat[0])*'=' + '+')


def cursor_to(y, x):
    print(f"\033[{y};{x}H")

if __name__ == "__main__":
    sys.exit(main(sys.argv))
