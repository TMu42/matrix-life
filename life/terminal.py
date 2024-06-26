import sys
import curses
import time


ZERO_R  = 121
ZERO_G  =   4
ZERO_B  = 180

ONE_R = 113
ONE_G = 805
ONE_B = 648

ZERO_DEFAULTS = [55, 17, 0]
ONE_DEFAULTS  = [49, 14, 6]


def initialize(args):
    global stdscr, running, paused, restore_cursor, colour_pair
    
    stdscr = curses.initscr()
    
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    
    stdscr.nodelay(True)
    
    colour_pair = _init_colours()
    
    restore_cursor = curses.curs_set(0)
    
    stdscr.keypad(True)
    
    field = _init_field(args)
    
    running = True
    
    paused = False
    
    return field


def _init_field(args):
    max_y, max_x = stdscr.getmaxyx()
    
    max_y -= 2
    max_x -= 2
    
    _h = min(max_y, args.resolution[1], args.size[1])
    _w = min(max_x, args.resolution[0], args.size[0])
    
    frame = stdscr.subwin(_h + 2, _w + 2, 0, 0)
    
    border = '╔' + _w*'═' + "╗\n"  \
     + (_h)*('║' + _w*' ' + "║\n") \
           + '╚' + _w*'═' + '╝'
    
    frame.insstr(0, 0, border, curses.color_pair(colour_pair))
    
    #stdscr.refresh()
    frame.refresh()
    
    return frame.subwin(_h, _w, 1, 1)


def _init_colours():
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
        return 0
    
    if curses.can_change_color():
        curses.init_color(bg, ZERO_R, ZERO_G, ZERO_B)
        curses.init_color(fg,  ONE_R,  ONE_G,  ONE_B)
    
    curses.init_pair(1, fg, bg)
    
    return 1


def end():
    if "stdscr" in globals() and stdscr is not None:
        stdscr.keypad(False)
    
    curses.curs_set(restore_cursor)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def paint_board(window, mat):
    width  = min(window.getmaxyx()[1], len(mat[0]))
    height = min(window.getmaxyx()[0], len(mat))
    
    for i in range(height):
        for j in range(width):
            s = '█' if mat[i, j] else ' '
            
            if j == width - 1:
                window.insstr(i, j, s, curses.color_pair(colour_pair))
            else:
                window.addstr(i, j, s, curses.color_pair(colour_pair))
            
    
    window.refresh()


def events():
    global running, paused
    
    try:
        while True:
            key = stdscr.get_wch()
            
            if key in ('\x1b', 'q', 'Q'):
                running = False
            elif key in ('p', 'P'):
                paused = not paused
    except curses.error:
        pass


def _get_info_lines(frame, count, sigmas):
    info_lines = 0
    
    if sigmas is not None:
        info_lines += len(sigmas)
    
    if frame is not None or count is not None:
        info_lines += 1
    
    return info_lines
