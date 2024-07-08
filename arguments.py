"""
This module provides command line options argument parsing for matrix-life.

Module arguments utilises python core argparse to handle command line
arguments, setting up an ArgumentParser specifically to handle arguments to
main.py which are useful for initializing a Model-View-Controller
configuration for a particular use case.

Constants:
DEFAULT     -- list of strings to indicate a default argument to an option.
NP_MATMUL   -- list of strings to indicate the NumPy Matmul algorithm to -A.
NP_ROLL     -- list of strings to indicate the NumPy Roll algorithm to -A.
SP_MATMUL   -- list of strings to indicate the SciPy Matmul algorithm to -A.
SP_CONVOLVE -- list of strings to indicate the SciPy Convolve algorithm to -A.
TERMINAL    -- list of strings to indicate the Terminal mode output to -O.
GRAPHICAL   -- list of strings to indicate the Graphical mode output to -O.

Functions:
get_args(argv)  -- obtain and preprocess arguments from argv.
_get_raw_args(args)
                -- initialize the ArgumentParser and parse arguments, Private.
_normalize_verbose_quiet(args)
                -- preprocess the verbose and quiet options, Private.
_normalize_size_resolution(args)
                -- preprocess the size and resolution options, Private.
"""

import argparse


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
    """
    Obtain and preprocess arguments from argv.
    
    This is the only Public function exposed by this module, it is not
    customizable or modifiable (without editing the Python code). This module
    has a single use case which is parsing command line arguments to main.py
    in this project. Pass sys.argv (including argv[0]) to get_args() to get a
    project specific argparse Namespace.
    
    Parameters:
    argv    -- list:    the argument list, usually sys.argv, Required.
    
    returns: Namespace  -- an object containing sensible values for all valid
                           command line arguments (see the doc for main.py).
    """
    args = _get_raw_args(argv)
    
#    _normalize_verbose_quiet(args)
    
    _normalize_size_resolution(args)
    
    return args


def _get_raw_args(args):
    """
    Obtain the "raw" Namespace object as provided by argparse.
    
    Appropriately initialize and ArgumentParser and parse args (excluding
    first element) through this.
    
    Parameters:
    args    -- list:    the argument list, usually sys.argv, Required.
    
    Returns: Namespace  -- an object containing "raw" values for all valid
                           command line arguments (see the doc for main.py).
    
    Note: This is a private function, you should not be calling this.
    """
    parser = argparse.ArgumentParser(prog="Matrix Life",
                                     description="Conway's Game of Life with "
                                                 "NumPy matrices")
    
    parser.add_argument('-v', "--verbose", action="count", default=0)
    parser.add_argument('-q', "--quiet",   action="count", default=0)
    
    parser.add_argument('-d', "--delay", type=float, default=DELAY)
    
    parser.add_argument('-r', "--resolution", type=int, nargs='+')
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
    """
    Preprocess the verbose and quiet flag options.
    
    -v and -q are count options on the ArgumentParser. "Sensible" behaviour if
    some of each are provided is to subtract each from the other (i.e.
    -qqv = -q : q = 1; v = -1and -vvqqvvqqvqvv = -vv : q = -2; v = 2). This
    function modifies the Namespace in place.
    
    Parameters:
    args    -- Namespace:   the object out of argparse, Required.
    
    Returns: None.
    
    Note: This is a private function, you should not be calling this.
    """
    quiet = args.quiet
    
    args.quiet -= args.verbose
    
    args.verbose -= quiet
    

def _normalize_size_resolution(args):
    """
    Preprocess the size and resolution options.
    
    -s and -r are multiple argument options on the ArgumentParser. Each option
    should result to a tuple of width and height. "Sensible" behaviour is: if
    one argument is received this should be width and height; if two arguments
    are recieved, these should be width and height respectively; if more than
    two arguments are recieved, behaviour is undefined. This function modifies
    the Namespace in place.
    
    Parameters:
    args    -- Namespace:   the object out of argparse, Required.
    
    Returns: None.
    
    Note: This is a private function, you should not be calling this.
    """
    #if len(args.resolution) == 1:
    #    args.resolution = tuple(2*args.resolution)
    #else:
    #    args.resolution = tuple(args.resolution[:2])
    #if len(args.size) == 1:
    #    args.size = tuple(2*args.size)
    #else:
    #    args.size = tuple(args.size[:2])
    
    if args.size is not None:
        args.size = (args.size[0], args.size[-1])
    if args.resolution is not None:
        args.resolution = (args.resolution[0], args.resolution[-1])
