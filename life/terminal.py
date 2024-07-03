import sys
import curses
import time

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


class TerminalView(mvc.View):
    def __init__(self, resolution=RESOLUTION, scale=None, position=(0, 0),
                       colours=COLOURS, **kwargs):
                       #fullscreen=False, icon_file=ICON_FILE,
                       #caption=CAPTION):
        self._matrix = None
        self._updates = False
        self._scale = scale
        self._position = position
        self._colours = colours
        #self._fullscreen = fullscreen
        
        self._init_curses(resolution)
        
        self._closed = False
    
    
    def update(self, matrix=None, flush=False):
        if self._closed:
            raise ValueError("Operation on closed View.")
        
        if matrix is not None and (matrix != self._matrix).any():
            self._matrix = matrix
            self._updates = True
        
        if flush and self._updates:
            _w = len(self._matrix[0])
            _h = len(self._matrix)
            
            for i in range(self._resolution[1]):
                for j in range(self._resolution[0]):
                    s = '█' if self._matrix[i%_h, j%_w] else ' '
                    
                    if j == self._resolution[0] - 1:
                        self._canvas.insstr(i, j, s,
                                       curses.color_pair(self._colour_pair))
                    else:
                        self._canvas.addstr(i, j, s,
                                       curses.color_pair(self._colour_pair))
            
            self._canvas.refresh()
    
    
    def close(self):
        if "stdscr" in globals() and stdscr is not None:
            stdscr.keypad(False)
        
        curses.curs_set(self._restore_cursor)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        
        self._closed = True
    
    
    def _init_curses(self, resolution=None):
        global stdscr
        
        stdscr = curses.initscr()
        
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        
        stdscr.nodelay(True)
        stdscr.keypad(True)
        
        self._restore_cursor = curses.curs_set(0)
        
        self._init_colours()
        self._init_field(resolution)
    
    
    def _init_colours(self):
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
    def handle_events(self):
        if self._closed:
            raise ValueError("Operation on closed Controller.")
        
        try:
            while True:
                key = stdscr.get_wch()
                
                if key in ('\x1b', 'q', 'Q'):
                    self._running = False
                elif key in ('p', 'P'):
                    self._paused = not self._paused
                #elif key in ('x', 'X'):
                #    raise ValueError("Invalid Key 'X'!")
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
