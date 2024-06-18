import sys
import time

import numpy as np
import scipy as sp


#MODE = "NUMPY_MATMUL"  # SLOW!!!!!
#MODE = "NUMPY_ROLL"
MODE = "SCIPY_MATMUL"

WIDTH  = 130
HEIGHT =  28

PRINT_WIDTH  = 130
PRINT_HEIGHT =  28

DELAY = 0.05

COUNT_END = 50

ONE = np.uint8(1)
ZRO = np.uint8(0)


if MODE == "NUMPY_MATMUL":
    L = np.roll(np.identity(WIDTH,  dtype=np.uint8), shift=1,  axis=1)
    R = np.roll(np.identity(WIDTH,  dtype=np.uint8), shift=-1, axis=1)
    U = np.roll(np.identity(HEIGHT, dtype=np.uint8), shift=1,  axis=0)
    D = np.roll(np.identity(HEIGHT, dtype=np.uint8), shift=-1, axis=0)
elif MODE == "SCIPY_MATMUL":
    #L = sp.sparse.eye_array(WIDTH,  k=1,  dtype=np.uint8)
    #R = sp.sparse.eye_array(WIDTH,  k=-1, dtype=np.uint8)
    #U = sp.sparse.eye_array(HEIGHT, k=1,  dtype=np.uint8)
    #D = sp.sparse.eye_array(HEIGHT, k=-1, dtype=np.uint8)
    
    L = sp.sparse.diags_array([[1], (WIDTH  - 1)*[1]], offsets=[1-WIDTH,   1])
    R = sp.sparse.diags_array([[1], (WIDTH  - 1)*[1]], offsets=[WIDTH-1,  -1])
    U = sp.sparse.diags_array([[1], (HEIGHT - 1)*[1]], offsets=[1-HEIGHT,  1])
    D = sp.sparse.diags_array([[1], (HEIGHT - 1)*[1]], offsets=[HEIGHT-1, -1])
    
    


def main(argv):
    rng = np.random.default_rng()
    
    world = rng.integers(2, size=[HEIGHT, WIDTH], dtype=np.uint8)
    
    #if MODE == "SCIPY_MATMUL":
    #    world = [row for row in world]
    
    sigma = sum(sum(world))
    count = 0
    
    frame = [0]
    
    print_board(world, frame, cls=False)
    
    try:
        while True:
            frame[-1] += 1
            
            print_board(world, frame)
            
            time.sleep(DELAY)
            #input()
            
            if sum(sum(world)) == sigma:
                count += 1
            else:
                sigma = sum(sum(world))
                
                count = 0
            if count == COUNT_END:
                world = rng.integers(2, size=[HEIGHT, WIDTH], dtype=np.uint8)
                
                frame += [0]
                
                continue
            
            if MODE == "NUMPY_MATMUL":
                world = life_step_np_matmul(world)
            elif MODE == "NUMPY_ROLL":
                world = life_step_np_roll(world)
            elif MODE == "SCIPY_MATMUL":
                world = life_step_sp_matmul(world)
            else:
                break
    except KeyboardInterrupt:
        cursor_to(HEIGHT + 3, 0)


def life_step_np_matmul(A):
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


def life_step_np_roll(A):
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


def life_step_sp_matmul(A):
    up_down = (U + D)@A
    lr_corn = (A + (U + D)@A)@(L + R)
    
    neighbours = up_down + lr_corn
    
    generate = np.minimum(neighbours//3, 1) - np.minimum(neighbours//4, 1)
    
    survive = (np.minimum(neighbours//2, 1) - np.minimum(neighbours//4, 1))
    
    return np.maximum(generate, A*survive)


def print_board(mat, frame=None, cls=True):
    if cls:
        cursor_to(1, 0)
    
    print(' +' + min(len(mat[0]), PRINT_WIDTH)*'=' + '+')
    
    for row in mat[:PRINT_HEIGHT]:
        print(' |', end='')
        
        for c in row[:PRINT_WIDTH]:
            print('#' if c else ' ', end='')
            #print(c, end='')
        
        print('|')
    
    print(' +' + min(len(mat[0]), PRINT_WIDTH)*'=' + '+')
    
    if frame is not None:
        f = frame[-10:]
        
        if len(f) < len(frame):
            f = ['...'] + f
        
        print(f"Frame: {sum(frame)} {f[::-1]}     ", end='')


def cursor_to(y, x):
    print(f"\033[{y};{x}H")

if __name__ == "__main__":
    sys.exit(main(sys.argv))
