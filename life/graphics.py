import numpy

from . import utils
from . import mvc

globals().update(utils.silent_import("pygame"))


ZERO_R =  31
ZERO_G =   1
ZERO_B =  46

ONE_R  =  29
ONE_G  = 206
ONE_B  = 166

RESOLUTION = (1280, 720)

COLOURS = [(ZERO_R, ZERO_G, ZERO_B), (ONE_R, ONE_G, ONE_B)]

ICON_FILE = "icon.ico"

CAPTION = "GraphicsView/Controller"


running = True
paused = False


class GraphicsView(mvc.View):
    def __init__(self, resolution=RESOLUTION, scale=None, position=(0, 0),
                       colours=COLOURS, fullscreen=False, icon_file=ICON_FILE,
                       caption=CAPTION):
        self._matrix = None
        self._updates = False
        self._resolution = (resolution[0], resolution[-1])
        self._scale = scale
        self._position = position
        self._colours = colours
        self._fullscreen = fullscreen
        
        pygame.init()
        
        try:
            icon = pygame.image.load(icon_file)
        except (TypeError, FileNotFoundError, pygame.error):
            try:
                icon = pygame.image.load(ICON_FILE)
            except (FileNotFoundError, pygame.error):
                pass
            else:
                pygame.display.set_icon(icon)
        else:
            pygame.display.set_icon(icon)
        
        if caption is not None:
            pygame.display.set_caption(caption)
        else:
            pygame.display.set_caption(CAPTION)
        
        if resolution is not None:
            self._resolution = (resolution[0], resolution[-1])
        else:
            self._resolution = RESOLUTION
        
        if fullscreen:
            self._canvas = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        else:
            self._canvas = pygame.display.set_mode(self._resolution,
                                                   flags=pygame.RESIZABLE)
    
    def update(self, matrix=None, flush=False):
        if matrix is not None and (matrix != self._matrix).any():
            self._matrix = matrix
            self._updates = True
        
        if flush and self._updates:
            r_pixels = (ONE_R - ZERO_R) \
                      *numpy.atleast_3d(self._matrix.T) + ZERO_R
            g_pixels = (ONE_G - ZERO_G) \
                      *numpy.atleast_3d(self._matrix.T) + ZERO_G
            b_pixels = (ONE_B - ZERO_B) \
                      *numpy.atleast_3d(self._matrix.T) + ZERO_B
            
            pixels = numpy.concatenate((r_pixels, g_pixels, b_pixels), axis=2)
            
            surface = pygame.surfarray.make_surface(pixels)
            
            surface = pygame.transform.scale(surface,
                                             self._canvas.get_rect()[2:])
            
            self._canvas.blit(surface, (0, 0))
            
            pygame.display.flip()
            
            self._updates = False
    
    def close(self):
        pygame.display.quit()
        pygame.quit()


class GraphicsController(mvc.Controller):
    def __init__(self, model=None):
        self._model = model
        
        self._running = True
        self._paused  = False
    
    def connect_model(self, model):
        self.model = model
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self._running = False
                elif event.key == pygame.K_p:
                    self._paused = not self._paused
            elif event.type == pygame.WINDOWMINIMIZED:
                self._paused = True
        
        if self._model is not None and self._running and not self._paused:
            self._model.step()
    
    def close(self):
        pass


########### Legacy #####################

def initialize(args):
    global running, paused
    
    pygame.init()
    
    icon = pygame.image.load("icon.ico")
    
    pygame.display.set_icon(icon)
    
    pygame.display.set_caption("Matrix Life")
    
    if args.fullscreen:
        surface = pygame.display.set_mode(flags=pygame.FULLSCREEN)
    else:
        surface = pygame.display.set_mode(args.resolution, pygame.RESIZABLE)
    
    running = True
    
    paused = args.paused
    
    return surface


def end():
    return


def paint_board(surface, mat):
    r_pixels = (ONE_R - ZERO_R)*numpy.atleast_3d(mat.T) + ZERO_R
    g_pixels = (ONE_G - ZERO_G)*numpy.atleast_3d(mat.T) + ZERO_G
    b_pixels = (ONE_B - ZERO_B)*numpy.atleast_3d(mat.T) + ZERO_B
    
    life_pixels = numpy.concatenate((r_pixels, g_pixels, b_pixels), axis=2)
    
    life_surface = pygame.surfarray.make_surface(life_pixels)
    
    life_surface = pygame.transform.scale(life_surface, surface.get_rect()[2:])
    
    surface.blit(life_surface, (0, 0))
    
    pygame.display.flip()


def events():
    global running, paused
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False
            elif event.key == pygame.K_p:
                paused = not paused
        elif event.type == pygame.WINDOWMINIMIZED:
            paused = True



