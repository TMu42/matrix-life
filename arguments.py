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
_normalize_colours(args)
                -- preprocess colours option, Private.
_add_colours(colour_map, colour_num, mode, values)
                -- add colours to a colour map
"""

import argparse


WIDTH  =  64
HEIGHT =  48

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
    
    _normalize_verbose_quiet(args)
    
    _normalize_size_resolution(args)
    
    _normalize_colours(args)
    
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
    
    parser.add_argument('-C', "--colours", "--colors", nargs='+')
    
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


def _normalize_colours(args):
    """
    Preprocess the colours option.
    
    -C is a  multiple argument option on the ArgumentParser. -C should resolve
    to a list of [bg_colour, fg_colour] or [colour_0, colour_1...colour_<n>]
    where each colour is itself either a single number (for palette or
    greyscale) or a tuple or (red, green, blue). "Sensible" behaviour is:
    Provide a language for specifying colours, accept the following keywords:
    
        "fg",       -- Everything that follows should be treated as specifying
        "bg",          fg_colour, bg_colour, colour_<n> until the next keyword
        "col<n>"       from this group. If these keywords are used, the first
                       argument should be one of these keywords and EVERY
                       colour must be specified with one of these keywords.
                       Values preceeding the first of these yield undefined
                       behaviour. Duplicate colour specifications also yeild'
                       undefined behaviour. Note: "bg" is a synonym for "col0"
                       and "fg" is a synonym for "col1". If these keywords are
                       not present, colours are read as an ordered list
                       starting with col0 (bg).
        
        "rgb",      -- The following 3, 4 numbers (range 0-255) should be
        "rgba"         treated as an rgb, rgba colour. If fewer than 3, 4
                       numbers are parsable, behaviour is undefined. If more
                       values are present, additional values are read as
                       seperate groups per behaviour below.
        
        "grey"      -- The following number should be treated as a greyscale
                       value (range 0-255). If there is no parsable number,
                       behaviour is undefined. If more values are present,
                       additional values are read as seperate groups per
                       behaviour below.

        "pal"       -- The following number should be treated as a palette
                       code (any range). If there is no parsable number,
                       behaviour is undefined. If more values are present,
                       additional values are read as seperate groups per
                       behaviour below.
    
    Values not preceeded by a keyword specifying the interpretation of the
    numbers are grouped in threes and read as rgb values if their quantity is
    a multiple of three, otherwise they are treated as singlets which may be
    interpreted as greyscale or pallette depending on View implementation.
    Values following the required group of a keyword are also treated as
    seperate lists however they will be assumed to follow the same format as
    the keyword they follow with additional values interpreted as singlets.
    Examples:
    
        `-C 7 5 3`                      --> [rgb(7,5,3), None].
        `-C 28 8`                       --> [28, 8].
        `-C grey 127 63 31`             --> [grey(127), grey(63), grey(31)].
        `-C rgb 255 127 63 63 127 255`  --> [rgb(255,127,63), rgb(63,127,255)].
        `-C rgb 99 88 77 pal 5`         --> [rgb(99,88,77), pal(5)].
        `-C rgb 99 88 77 5`             --> [rgb(99,88,77), 5].
        `-C fg 100 50 25 bg 90 60 30`   --> [rgb(90,60,30), rgb(100,50,25)].
        `-C fg 9`                       --> [None, 9].
        `-C col2 grey 100 bg pal 6`     --> [pal(6), None, grey(100)].
    
    The availability of any given colour system or how it should be handled is
    up to the specification of the invoked View object.
    
    Parameters:
    args    -- Namespace:   the object out of argparse, Required.
    
    Returns: None.
    
    Note: This is a private function, you should not be calling this.
    """
    colour_map = {}
    
    colour_num = 0
    
    mode = None
    
    values = []
    
    for word in args.colours + [None]:
        try:
            n = int(word)
        except TypeError:
            _add_colours(colour_map, colour_num, mode, values)
        except ValueError:
            colour_num += _add_colours(colour_map, colour_num, mode, values)
            
            values = []
            
            mode = None
            
            if word == "bg":
                colour_num = 0
                
                mode = "greedy"
            elif word == "fg":
                colour_num = 1
                
                mode = "greedy"
            elif word[:3] == "col":
                try:
                    colour_num = int(word[3:])
                except ValueError:
                    raise ValueError(
                                f"{word} is not a valid keyword or integer.")
                
                mode = "greedy"
            elif word in ("rgb", "rgba", "grey", "pal"):
                mode = word
            else:
                raise ValueError(f"{word} is not a valid keyword or integer.")
        else:
            values += [n]
    
    args.colours = colour_map


def _add_colours(colour_map, colour_num, mode, values):
    """
    Add colours to a colour map.
    
    Helper function for _normalize_colours(), add a list of values as colours,
    interpreted based on the mode value, starting from colour_number.
    
    Parameters:
    colour_mop  -- dict:    the colour map, Required.
    colour_num  -- int:     the number of the (first) colour to add, Required.
    mode        -- str:     the mode indicator, one of: "rgba", "rgb", "grey",
                            "pal" or None, Required.
    values      -- list:    a list of ints to process into colours, Required.
    
    Returns: int    -- the number of colours added to colour_map.
    
    Note: This is a private function, you should not be calling this.
    """
    start_index = colour_num
    
    if mode is None and (len(values)%3 == 0):
        mode = "rgb"
    elif mode == "greedy":
        if len(values) >= 3 and ((len(values)%3 == 0) or
                                 (len(values)%4 != 0)):
            mode = "rgb"
        elif len(values) >= 4:
            mode = "rgba"
        else:
            mode = None
    
    if mode == "rgba":
        while len(values) >= 4:
            colour_map[colour_num] = tuple(["rgba"] + values[:4])
            
            values = values[4:]
            
            colour_num += 1
        
        while len(values) != 0:
            colour_map[colour_num] = tuple([None, values[0]])
            
            values = values[1:]
            
            colour_num += 1
    elif mode == "rgb":
        while len(values) >= 3:
            colour_map[colour_num] = tuple(["rgb"] + values[:3])
            
            values = values[3:]
            
            colour_num += 1
        
        while len(values) != 0:
            colour_map[colour_num] = tuple([None, values[0]])
            
            values = values[1:]
            
            colour_num += 1
    else:
        while len(values) != 0:
            colour_map[colour_num] = tuple([mode, values[0]])
            
            values = values[1:]
            
            colour_num += 1
    
    return colour_num - start_index





################## END OF FILE ############################
