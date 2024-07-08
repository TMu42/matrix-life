"""
Terminal View-Controller for cellular automata Models with (n)curses.

This module provides the View and Controller elements of a
Model-View-Controller design pattern for operating cellular automata. Python's
curses binding is used to manage character based terminal output displays and
also user input event handling.

Classes:
TerminalView        -- A View for terminal rendering of cellular automata.
TerminalController  -- A Controller to pair with a TerminalView object.
"""

import sys
import curses

from . import mvc


ZERO_R  = 121
ZERO_G  =   4
ZERO_B  = 180

ONE_R = 113
ONE_G = 805
ONE_B = 648

COLOURS = [(ZERO_R, ZERO_G, ZERO_B), (ONE_R, ONE_G, ONE_B)]

ZERO_DEFAULTS = [55, 17, 0]
ONE_DEFAULTS  = [49, 14, 6]


RESOLUTION = None   #(132, 32)

SCALE = 1

# Curses constants seem to be incorrect so we provide these alternatives,
# these may not be very cross-platform compatible as they were detected
# empirically.
KEY_A1 = 262
KEY_A3 = 339
KEY_B2 = 591
KEY_C1 = 360
KEY_C3 = 338



class TerminalView(mvc.View):
    """
    A View class implementing rendering of cellular automata with curses.
    
    This class handles initialization, output operation and termination of a
    curses instance for the express purpose of rendering cellular automata in
    the form of Model objects. This class is intended to be used with
    compatible Model and Controller objects as part of a Model-View-Controller
    deign pattern. It is recommended to use the accompanying TerminalController
    class which handles user input from the curses instance.
    
    Extends:
    .mvc.View   -- Abstract Base Class for Views in the Model-View-Controller.
    
    Instance Variables:
    _canvas     -- window:  the output curses sub window.
    _closed     -- bool:    the object has been terminated.
    _colours    -- list:    the display colour scheme.
    _matrix     -- ndarray: the most recently provided automata state.
    _position   -- tuple:   coordinates for the top left corner of _matrix.
    _resolution -- tuple:   the size of the curses window _canvas.
    _scale      -- float:   the zoom factor in characters/cell.
    _updates    -- bool:    flag to indicate _matrix has updates not yet
                            flushed to _canvas.
    
    Methods:
    __init__(self[, resolution][, scale][, position][, colours][, **kwargs])
            -- Initialize class object, override View.__init__().
    close(self)
            -- Decommission, deactivate and delete the object,
               override View.close().
    scale(self, delta)
            -- Scale the view by some delta, Not Implemented.
    scale_to(self, value)
            -- Scale the view to a value, Not Implemented.
    update(self[, matrix][, flush])
            -- Update and/or draw the matrix, override View.update().
    _init_colours(self)
            -- Initialize the curses colour pair scheme, Private.
    _init_curses(self[, resolution])
            -- Initialize the curses instance, Private.
    _init_field(self[, resolution])
            -- Initialize the border and subwin _canvas, Private.
    
    Inherits:
    View.move(self, distance)
            -- Move the view coordinates by a relative amount or distance.
    View.move_to(self, position)
            -- Move the view coordinates to an absolute position.
    
    Warning:
    Any assignment to instance variables or calls to private methods will
    result in the object entering an illegal and potentially unrecoverable
    state or worse, render the terminal unusable.
    """
    
    def __init__(self, resolution=None, scale=None, position=(0, 0),
                       colours=COLOURS, **kwargs):
        """
        Initialize TerminalView object.
        
        Overrides:
        View.__init__() -- Abstract Base Class initializer.
        
        Parameters:
        self        -- TerminalView:
                                the object itself, Required.
        resolution  -- tuple:   the resolution of the view screen,
                                Default = None.
        scale       -- float:   the scale of the view screen in
                                characters/cell, Default = None.
        position    -- tuple:   the starting coordinates for the top-left of
                                matrix, Default = (0, 0).
        colours     -- list:    the colour scheme for cell values,
                                Default = [(121, 4, 180), (113, 805, 648)].
        **kwargs    -- dict:    catch any additional arguments intended for
                                other implementations of View if they should
                                go through to the keeper.
        
        Returns: None.
        """
        if resolution is None:
            resolution = RESOLUTION
        
        if scale is None:
            scale = SCALE
        
        self._matrix = None
        self._updates = False
        self._resolution = resolution
        self._scale = scale
        self._position = position
        self._colours = colours
        
        self._init_curses(resolution)
        
        self._closed = False
    
    
    def update(self, matrix=None, flush=False):
        """
        Update the internal matrix and/or flush to the view window.
        
        Overrides:
        View.update()   -- Abstract Base Class API method.
        
        This method is primarily for painting or preparing to paint the screen.
        
        Parameters:
        self    -- TerminalView:
                            the object itself, Required.
        matrix  -- array:   the new matrix data, Default = None.
        flush   -- bool:    whether to output to view window, Default = False.
        
        Returns None.
        
        Exceptions Raised:
        ValueError  -- if self has already been closed with self.close().
        """
        if self._closed:
            raise ValueError("Operation on closed View.")
        
        if matrix is not None and (matrix != self._matrix).any():
            self._matrix = matrix
            self._updates = True
        
        if flush and self._updates:
            _w = len(self._matrix[0])
            _h = len(self._matrix)
            
            _x = self._position[0]%_w
            _y = self._position[1]%_h
            
            for i in range(self._resolution[1]):
                for j in range(self._resolution[0]):
                    # = "\x1B[38;2;255;0;0m"
                    s = ('█' if self._matrix[(i - _y)%_h, (j - _x)%_w] \
                    else ' ')
                    # + "\x1B[39;49m"
                    
                    if j == self._resolution[0] - 1:
                        self._canvas.insstr(i, j, s,
                                       curses.color_pair(self._colour_pair))
                    else:
                        self._canvas.addstr(i, j, s,
                                       curses.color_pair(self._colour_pair))
            
            self._canvas.refresh()
    
    
    def close(self):
        """
        Decommission, deactivate and delete the object permanently.
        
        This method closes the curses instance and sets the _closed flag to
        prevent further operations on self.
        
        Overrides:
        View.close()    -- Abstract Base Class destructor.
        
        Parameters:
        self    -- TerminalView:    the object itself, Required.
        
        Returns None.
        """
        if "stdscr" in globals() and stdscr is not None:
            stdscr.keypad(False)
        
        curses.curs_set(self._restore_cursor)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        
        self._closed = True
    
    
    def _init_curses(self, resolution=None):
        """
        Initialize the curses instance in the current terminal.
        
        Perform curses initialization, saving state where necessary to restore
        at close(). Field and colour initialization is also performed by calls
        to these private methods.
        
        Parameters:
        self        -- TerminalView:
                                the object itself, Required.
        resolution  -- tuple:   the requested screen resolution,
                                Default = None.
        
        Returns: None.
        
        Note:
        This is a private "helper" method, externally this operation should be
        performed by a call to __init__() or more correctly, by default
        instanciation of a TerminalView object. External calls to this method
        may leave the object in an illegal, unrecoverable state or worse,
        render the terminal unusable.
        """
        global stdscr
        
        stdscr = curses.initscr()
        
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        
        # DEBUG
        #sys.stderr.write(
        #    f"Extended Colours:\t{curses.has_extended_color_support()}\r\n")
        #sys.stderr.write(f"Colours:\t\t{curses.COLORS}\r\n")
        #sys.stderr.write(f"Colour Pairs:\t\t{curses.COLOR_PAIRS}\r\n")
        #sys.stderr.flush()
        
        stdscr.nodelay(True)
        stdscr.keypad(True)
        
        self._restore_cursor = curses.curs_set(0)
        
        self._init_colours()
        self._init_field(resolution)
    
    
    def _init_colours(self):
        """
        Initialize the curses colour pairs.
        
        Attempt to emmulate the requested colour scheme by initializing colour
        pairs in curses to a best available match.
        
        Parameters:
        self        -- TerminalView:    the object itself, Required.
        
        Returns: None.
        
        Note:
        This is a private "helper" method, externally this operation should be
        performed by a call to __init__() or more correctly, by default
        instanciation of a TerminalView object. External calls to this method
        may leave the object in an illegal, unrecoverable state or worse,
        render the terminal unusable.
        """
        fg, bg = None, None
        
        for col in ZERO_DEFAULTS:
            if col < curses.COLORS:
                bg = col
                
                break
        
        for col in ONE_DEFAULTS:
            if col < curses.COLORS:
                fg = col
                
                break
        
        if fg is None or bg is None or not curses.COLOR_PAIRS > 1:
            self._colour_pair = 0
            
            return
        
        if curses.can_change_color():
            curses.init_color(bg, *self._colours[0])#ZERO_R, ZERO_G, ZERO_B)
            curses.init_color(fg, *self._colours[1])# ONE_R,  ONE_G,  ONE_B)
        
        curses.init_pair(1, fg, bg)
        
        self._colour_pair = 1
    
    
    def _init_field(self, resolution=None):
        """
        Initialize the curses sub-window _canvas and the border.
        
        Perform a best match to the requested resolution for the current
        terminal. Save this window in _canvas and paint the border.
        
        Parameters:
        self        -- TerminalView:
                                the object itself, Required.
        resolution  -- tuple:   the requested screen resolution,
                                Default = None.
        
        Returns: None.
        
        Note:
        This is a private "helper" method, externally this operation should be
        performed by a call to __init__() or more correctly, by default
        instanciation of a TerminalView object. External calls to this method
        may leave the object in an illegal, unrecoverable state or worse,
        render the terminal unusable.
        """
        max_h, max_w = stdscr.getmaxyx()
        
        max_h -= 2
        max_w -= 2
        
        if resolution is None:
            _w, _h = max_w, max_h
        else:
            _w, _h = min(max_w, resolution[0]), min(max_h, resolution[1])
        
        self._resolution = (_w, _h)
        
        frame = stdscr.subwin(_h + 2, _w + 2, 0, 0)
        
        border = '╔' + _w*'═' + "╗\n"  \
         + (_h)*('║' + _w*' ' + "║\n") \
               + '╚' + _w*'═' + '╝'
        
        frame.insstr(0, 0, border, curses.color_pair(self._colour_pair))
        
        frame.refresh()
        
        self._canvas = frame.subwin(_h, _w, 1, 1)


class TerminalController(mvc.Controller):
    """
    A Controller class implementing curses event handling on cellular automata.
    
    This class does not manage the curses instance but provides Controller API
    handling of curses input as well as the rest of the Controller API. This
    class is intended for use with a TerminalView object providing management
    of the underlying curses instance. This class is intended to be used with
    compatible Model and View objects as part of a Model-View-Controller
    design pattern. It is not recommended to use this class without attaching
    a TerminalView object as behaviour is likely to be unexpected and
    undesirable.
    
    Extends:
    .mvc.Controller -- Abstract Base Class for Controllers in the
                       Model-View-Controller.
    
    Instance Variables:
    _model      -- Model:   the Model object to run.
    _view       -- View:    the View object to update and adjust.
    _delay      -- float:   additional delay in seconds added to each loop.
    _running    -- bool:    the automaton is not finished.
    _paused     -- bool:    the automaton is paused.
    _closed     -- bool:    the object has been terminated.
    
    Methods:
    handle_events(self)
            -- Handle curses events, specifically user input,
               override Controller.handle_events()
    
    Inherits:
    Controller.__init__(self[, model][, view][, delay][, **kwargs])
            -- Initialize class object.
    Controller.close(self)
            -- Decommission, deactivate and delete the object.
    Controller.connect_model(self, model)
            -- Connect a Model object to the Controller.
    Controller.connect_view(self, view)
            -- Connect a View object to the Controller.
    Controller.run(self)
            -- Run the main control loop.
    
    Warning:
    Any assignment to instance variables or calls to private methods will
    result in the object entering an illegal and potentially unrecoverable
    state or worse, render the terminal unusable.
    """
    
    def handle_events(self):
        """
        Handle curses asynchronous input to provide user interactivity.
        
        This method provides proper handling of asynchronous curses input and
        detects property changes to provided canonical user input and
        adaptability to window state.
        
        Parameters:
        self    -- TerminalController:  the object itself, Required.
        
        Returns None.
        
        Exceptions Raised:
        ValueError  -- if self has already been closed with self.close().
        """
        if self._closed:
            raise ValueError("Operation on closed Controller.")
        
        try:
            while True:
                key = stdscr.get_wch()
                
                if key in ('\x1b', 'q', 'Q'):
                    self._running = False
                elif key in (' ', 'p', 'P'):
                    self._paused = not self._paused
                elif key in ('\r', '\n', 's', 'S'):
                    self._step = True
                elif key in (curses.KEY_UP, '8'):
                    self._view.move(( 0,  1))
                elif key in (curses.KEY_DOWN, '2'):
                    self._view.move(( 0, -1))
                elif key in (curses.KEY_LEFT, '4'):
                    self._view.move(( 1,  0))
                elif key in (curses.KEY_RIGHT, '6'):
                    self._view.move((-1,  0))
                elif key in (curses.KEY_A1, KEY_A1, '7'):  # UP-LEFT
                    self._view.move(( 1,  1))
                elif key in (curses.KEY_A3, KEY_A3, '9'):  # UP-RIGHT
                    self._view.move((-1,  1))
                elif key in (curses.KEY_C1, KEY_C1, '1'):  # DOWN-LEFT
                    self._view.move(( 1, -1))
                elif key in (curses.KEY_C3, KEY_C3, '3'):  # DOWN-LEFT
                    self._view.move((-1, -1))
                elif key in (curses.KEY_B2, KEY_B2, '5'):  # MIDDLE
                    self._view.move_to((0, 0))
                #else:
                #    sys.stderr.write(
                #            f"{sys.argv[0]}: Unregistered key: {key}\n")
        
        except curses.error:
            pass


############# Legacy ##############################################

#def _get_info_lines(frame, count, sigmas):
#    info_lines = 0
#    
#    if sigmas is not None:
#        info_lines += len(sigmas)
#    
#    if frame is not None or count is not None:
#        info_lines += 1
#    
#    return info_lines



################## END OF FILE ############################
