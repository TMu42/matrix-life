import sys

import numpy as np


def main(argv):
    rng = np.random.default_rng()
    
    world = rng.integers(2, size=[100, 100], dtype=np.uint8)
    
    print(world[30:60,30:60])




if __name__ == "__main__":
    sys.exit(main(sys.argv))
