import sys
import time

import numpy as np


WIDTH  = 130
HEIGHT = 28

DELAY = 0.01

COUNT_END = 50

def main(argv):
    rng = np.random.default_rng()
    
    world = rng.integers(2, size=[HEIGHT, WIDTH], dtype=np.uint8)
    
    sigma = sum(sum(world))
    count = 0
    
    print_board(world, cls=False)
    
    try:
        while True:
            print_board(world)
            
            time.sleep(DELAY)
            
            
            if sum(sum(world)) == sigma:
                count += 1
            else:
                sigma = sum(sum(world))
                
                count = 0
            if count == COUNT_END:
                world = rng.integers(2, size=[HEIGHT, WIDTH], dtype=np.uint8)
                
                continue
            
            world = life_step(world)
    except KeyboardInterrupt:
        cursor_to(HEIGHT + 3, 0)


def life_step(A):
    L = np.roll(np.identity(A.shape[1], dtype=np.uint8), shift=1,  axis=1)
    R = np.roll(np.identity(A.shape[1], dtype=np.uint8), shift=-1, axis=1)
    U = np.roll(np.identity(A.shape[0], dtype=np.uint8), shift=1,  axis=0)
    D = np.roll(np.identity(A.shape[0], dtype=np.uint8), shift=-1, axis=0)
    
    left       =   A@L
    right      =   A@R
    up         = U@A
    down       = D@A
    up_left    = U@A@L
    up_right   = U@A@R
    down_left  = D@A@L
    down_right = D@A@R
    
    neighbours = left  + up   + up_left  + down_left \
               + right + down + up_right + down_right
    
    ONE = np.uint8(1)
    ZRO = np.uint8(0)
    
    itrA = np.nditer(A)
    itrN = np.nditer(neighbours)
    
    return np.array([ONE if (a == 1 and n > 1 and n < 4) or n == 3 else ZRO \
                               for a, n in zip(itrA, itrN)]).reshape(A.shape)


def print_board(mat, cls=True):
    if cls:
        cursor_to(1, 0)
    
    print(' +' + len(mat[0])*'=' + '+')
    for row in mat:
        print(' |', end='')
        for c in row:
            print('#' if c else ' ', end='')
        print('|')
    print(' +' + len(mat[0])*'=' + '+')


def cursor_to(y, x):
    print(f"\033[{y};{x}H")

if __name__ == "__main__":
    sys.exit(main(sys.argv))
