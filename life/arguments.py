import argparse
import shutil


WIDTH  = 130
HEIGHT =  28

DELAY = 0.05


def get_args(args):
    args = _get_raw_args(args)
    
    args = _normalize_verbose_quiet(args)
    
    args = _normalize_width_height_delay(args)
    
    args = _normalize_algorithm(args)
    
    return args


def _get_raw_args(args):
    parser = argparse.ArgumentParser(prog="Matrix Life",
                                     description="Conway's Game of Life with "
                                                 "NumPy matrices")
    
    parser.add_argument('-v', "--verbose", action="count", default=0)
    parser.add_argument('-q', "--quiet",   action="count", default=0)
    
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
    
    return parser.parse_args(args=args[1:])


def _normalize_verbose_quiet(args):
    quiet = args.quiet
    
    args.quiet -= args.verbose
    
    args.verbose -= quiet
    
    return args


def _normalize_width_height_delay(args):
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
    
    if args.width == 0:
        terminal_size = shutil.get_terminal_size()
        
        args.width = terminal_size.columns - 2
    
    if args.height == 0:
        terminal_size = shutil.get_terminal_size()
        
        if args.verbose < 0:
            info_lines = 0
        elif args.verbose < 2:
            info_lines = 1
        else:
            info_lines = 5
        
        args.height = terminal_size.lines - (4 + info_lines)
    
    return args

def _normalize_algorithm(args):
    if args.algorithm is None:
        args.algorithm = 0
    else:
        args.algorithm = int(args.algorithm)
    
    return args