import sys

import numpy as np



KERNEL = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]])


def main(argv):
    rng = np.random.default_rng()
    
    world = rng.integers(2, size=[20, 20], dtype=np.uint8)
    
    while True:
        print(world[:,:])
        
        if input() == 'q':
            break
    
        life_step(world)
    

def life_step(A):
    L = np.roll(np.identity(A.shape[0], dtype=np.uint8), shift=1,  axis=0)
    R = np.roll(np.identity(A.shape[0], dtype=np.uint8), shift=-1, axis=0)
    U = np.roll(np.identity(A.shape[1], dtype=np.uint8), shift=1,  axis=1)
    D = np.roll(np.identity(A.shape[1], dtype=np.uint8), shift=-1, axis=1)
    
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
    
    with np.nditer(A, op_flags=["readwrite"]) as itrA, \
         np.nditer(neighbours) as itrN:
        for a, n in zip(itrA, itrN):
            a[...] = (ONE if (a == 1 and n > 1 and n < 4) or n == 3 else ZRO)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
