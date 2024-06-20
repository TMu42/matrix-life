import sys
import shutil


def prepare_terminal():
    terminal_size = shutil.get_terminal_size()
    
    print((terminal_size.lines - 2)*'\n', end='')


def end_terminal(mat, frame=None, count=None, sigmas=None):
    terminal_size = shutil.get_terminal_size()
    
    info_lines = _get_info_lines(frame, count, sigmas)
    
    end = min(terminal_size.lines - (4 + info_lines), len(mat)) \
                                                        + info_lines + 4
    
    _cursor_to(end, 1)


def print_board(mat, frame=None, count=None, sigmas=None, cls=True):
    terminal_size = shutil.get_terminal_size()
    
    info_lines = _get_info_lines(frame, count, sigmas)
    
    print_width  = min(terminal_size.columns - 2, len(mat[0]))
    print_height = min(terminal_size.lines - (4 + info_lines), len(mat))
    
    if cls:
        _cursor_to(2, 1)
    
    print('+' + print_width*'=' + '+')
    
    for row in mat[:print_height]:
        print('|', end='')
        
        for c in row[:print_width]:
            print('#' if c else ' ', end='')
            #print(c, end='')
        
        print('|')
    
    print('+' + min(len(mat[0]), print_width)*'=' + '+')
    
    if sigmas is not None:
        for key in sigmas:
            print(f"{key}: {sigmas[key]}  ")
    
    if frame is not None:
        f = frame[-10:]
        
        if len(f) < len(frame):
            f = ['...'] + f
        
        print(f"Frame: {sum(frame)} {f[::-1]}    ", end='')
    
    if count is not None:
        print(f"Count: {count}    ", end='')
    
    sys.stdout.flush()


def _cursor_to(y, x):
    print(f"\033[{y};{x}H", end='')
    
    sys.stdout.flush()


def _get_info_lines(frame, count, sigmas):
    info_lines = 0
    
    if sigmas is not None:
        info_lines += len(sigmas)
    
    if frame is not None or count is not None:
        info_lines += 1
    
    return info_lines
