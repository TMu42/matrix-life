import argparse
import shutil


WIDTH  =  96
HEIGHT =  54

DELAY = 0.05

DEFAULT   = ["default", "def", "deflt", "dflt", 'd']

NP_MATMUL   = ["numpy-matmul","np-matmul", "n-matmul", "nm",
               "numpy", "np", 'n']
NP_ROLL     = ["numpy-roll", "np-roll", "n-roll", "nr", "roll", 'r']
SP_MATMUL   = ["scipy-matmul", "sparse-matmul", "sp-matmul", "s-matmul", "sm",
               "scipy", "sparse", "sp", 's',
               "matmul", 'm']
SP_CONVOLVE = ["scipy-convolve", "scipy-conv", "sp-convolve", "sp-conv", "sc",
               "convolve", "conv", 'c']

TERMINAL  = ["terminal", "term", 't', "ncurses", "nc", "curses", 'c']
GRAPHICAL = ["graphical", "graph", 'g', "pygame", "pg", 'p']

ALGORITHMS = DEFAULT + NP_MATMUL + NP_ROLL + SP_MATMUL + SP_CONVOLVE

OUTPUTS = DEFAULT + TERMINAL + GRAPHICAL

RES_WIDTH  = 960
RES_HEIGHT = 540

#MAX_RESOLUTION_WIDTH  = 1280
#MAX_RESOLUTION_HEIGHT =  720

#MIN_RESOLUTION_WIDTH  = 160
#MIN_RESOLUTION_HEIGHT =  90


def get_args(argv):
    args = _get_raw_args(argv)
    
#    _normalize_verbose_quiet(args)
    
    _normalize_size_resolution(args)
    
    return args


def _get_raw_args(args):
    parser = argparse.ArgumentParser(prog="Matrix Life",
                                     description="Conway's Game of Life with "
                                                 "NumPy matrices")
    
    parser.add_argument('-v', "--verbose", action="count", default=0)
    parser.add_argument('-q', "--quiet",   action="count", default=0)
    
    parser.add_argument('-d', "--delay", type=float, default=DELAY)
    
    parser.add_argument('-r', "--resolution", type=int, nargs='+',
                                              default=[RES_WIDTH, RES_HEIGHT])
    parser.add_argument('-s', "--size",       type=int, nargs='+',
                                              default=[WIDTH, HEIGHT])
    
    parser.add_argument('-A', "--algorithm", choices=ALGORITHMS,
                                             default=DEFAULT[0])
    
    parser.add_argument('-O', '--outmode', choices=OUTPUTS,
                                           default=DEFAULT[0])
    
    parser.add_argument('-p', "--paused",     action="store_true")
    parser.add_argument('-F', "--fullscreen", action="store_true")
    
    return parser.parse_args(args=args[1:])


def _normalize_verbose_quiet(args):
    quiet = args.quiet
    
    args.quiet -= args.verbose
    
    args.verbose -= quiet
    

def _normalize_size_resolution(args):
    #if len(args.resolution) == 1:
    #    args.resolution = tuple(2*args.resolution)
    #else:
    #    args.resolution = tuple(args.resolution[:2])
    #if len(args.size) == 1:
    #    args.size = tuple(2*args.size)
    #else:
    #    args.size = tuple(args.size[:2])
    
    args.size       = (args.size[0],       args.size[-1])
    args.resolution = (args.resolution[0], args.resolution[-1])
