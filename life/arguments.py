import argparse
import shutil


WIDTH  = 130
HEIGHT =  28

DELAY = 0.05

DEFAULT   = ["default", "def", 'd']

NP_MATMUL   = ["numpy-matmul","np-matmul", "n-matmul", "nm",
               "numpy", "np", 'n']
NP_ROLL     = ["numpy-roll", "np-roll", "n-roll", "nr", 'r']
SP_MATMUL   = ["scipy-matmul", "sp-matmul", "s-matmul", "sm",
               "scipy", "sp", 's',
               "matmul", 'm']
SP_CONVOLVE = ["scipy-convolve", "scipy-conv", "sp-convolve", "sp-conv", "sc",
               "convolve", "conv", 'c']

TERMINAL  = ["terminal", "term", 't', "curses"]
GRAPHICAL = ["graphical", "graph", 'g', "pygame"]

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
    
    _normalize_verbose_quiet(args)
    
    _normalize_size_resolution(args)
    
    _normalize_algorithm(args)
    
    _normalize_outmode(args)
    
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
    
    parser.add_argument('-F', "--fullscreen", action="store_true")
    
    #parser.add_argument('-R', "--numpy-roll", action="store_const",
    #                                          dest="algorithm",
    #                                          const=0)
    #parser.add_argument('-M', "--numpy-matmul", action="store_const",
    #                                            dest="algorithm",
    #                                            const=1)
    #parser.add_argument('-S', "--scipy-matmul", action="store_const",
    #                                            dest="algorithm",
    #                                            const=2)
    #parser.add_argument('-C', "--scipy-convolve", action="store_const",
    #                                              dest="algorithm",
    #                                              const=3)
    
    return parser.parse_args(args=args[1:])


def _normalize_verbose_quiet(args):
    quiet = args.quiet
    
    args.quiet -= args.verbose
    
    args.verbose -= quiet
    

def _normalize_size_resolution(args):
    if len(args.resolution) == 1:
        args.resolution = tuple(2*args.resolution)
    else:
        args.resolution = tuple(args.resolution[:2])
    if len(args.size) == 1:
        args.size = tuple(2*args.size)
    else:
        args.size = tuple(args.size[:2])


def _normalize_algorithm(args):
    if args.algorithm in DEFAULT:
        args.algorithm = NP_ROLL[0]
    elif args.algorithm in NP_MATMUL:
        args.algorithm = NP_MATMUL[0]
    elif args.algorithm in NP_ROLL:
        args.algorithm = NP_ROLL[0]
    elif args.algorithm in SP_MATMUL:
        args.algorithm = SP_MATMUL[0]
    elif args.algorithm in SP_CONVOLVE:
        args.algorithm = SP_CONVOLVE[0]
#    if args.algorithm is None:
#        args.algorithm = 0
#    else:
#        args.algorithm = int(args.algorithm)
#    
#    return args


def _normalize_outmode(args):
    if args.outmode in DEFAULT:
        args.outmode = TERMINAL[0]
#    if args.outmode is None:
#        args.outmode = 0
#    else:
#        args.outmode = int(args.outmode)
#    
#    return args
