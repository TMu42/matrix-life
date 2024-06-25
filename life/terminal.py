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
    
    time.sleep(2)
    
    running = True
    
    paused = False
    
    return field


def _init_field(args):
    frame = stdscr.subwin(curses.LINES, curses.COLS, 0, 0)
    
    _h, _w = frame.getmaxyx()
    
    _h -= 2
    _w -= 2
    
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


def end(stdscr=None):
    if stdscr is not None:
        stdscr.keypad(False)
    
    curses.curs_set(restore_cursor)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def paint_board(window, mat):
    window.addstr(10, 10, '$$')
    
    window.refresh()


#def print_board(mat, frame=None, count=None, sigmas=None, cls=True):
#    terminal_size = shutil.get_terminal_size()
#    
#    info_lines = _get_info_lines(frame, count, sigmas)
#    
#    print_width  = min(terminal_size.columns - 2, len(mat[0]))
#    print_height = min(terminal_size.lines - (4 + info_lines), len(mat))
#    
#    if cls:
#        _cursor_to(2, 1)
#    
#    print('+' + print_width*'=' + '+')
#    
#    for row in mat[:print_height]:
#        print('|', end='')
#        
#        for c in row[:print_width]:
#            print('#' if c else ' ', end='')
#            #print(c, end='')
#        
#        print('|')
#    
#    print('+' + min(len(mat[0]), print_width)*'=' + '+')
#    
#    if sigmas is not None:
#        for key in sigmas:
#            print(f"{key}: {sigmas[key]}  ")
#    
#    if frame is not None:
#        f = frame[-10:]
#        
#        if len(f) < len(frame):
#            f = ['...'] + f
#        
#        print(f"Frame: {sum(frame)} {f[::-1]}    ", end='')
#    
#    if count is not None:
#        print(f"Count: {count}    ", end='')
#    
#    sys.stdout.flush()


def events():
    global running, paused
    
    try:
        while True:
            key = stdscr.getkey()
            
            if key in ("KEY_ESC", 'q'):
                running = False
    except curses.error:
        pass


def _get_info_lines(frame, count, sigmas):
    info_lines = 0
    
    if sigmas is not None:
        info_lines += len(sigmas)
    
    if frame is not None or count is not None:
        info_lines += 1
    
    return info_lines
