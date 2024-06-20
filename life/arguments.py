import argparse


WIDTH  = 130
HEIGHT =  28

DELAY = 0.05


def get_args(args):
    parser = argparse.ArgumentParser(prog="Matrix Life",
                                     description="Conway's Game of Life with "
                                                 "NumPy matrices")
    
    parser.add_argument('-W', "--width")
    parser.add_argument('-H', "--height")
    parser.add_argument('-D', "--delay")
    parser.add_argument('-R', "--numpy-roll", action="store_const",
                                              dest="algorithm",
                                              const=0)
    parser.add_argument('-M', "--numpy-matmul", action="store_const",
                                                dest="algorithm",
                                                const=1)
    parser.add_argument('-S', "--scipy-matmul", action="store_const",
                                                dest="algorithm",
                                                const=2)
    parser.add_argument('-C', "--scipy-convolve", action="store_const",
                                                  dest="algorithm",
                                                  const=3)
    
    args = parser.parse_args(args=args[1:])
    
    if args.width is None:
        args.width = WIDTH
    else:
        args.width = int(args.width)
    
    if args.height is None:
        args.height = HEIGHT
    else:
        args.height = int(args.height)
    
    if args.delay is None:
        args.delay = DELAY
    else:
        args.delay = float(args.delay)
    
    if args.algorithm is None:
        args.algorithm = 0
    else:
        args.algorithm = int(args.algorithm)
    
    return args
