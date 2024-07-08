"""
Graphical View-Controller for cellular automata Models with PyGame.

This module provides the View and Controller elements of a
Model-View-Controller design pattern for operating cellular automata. PyGame
is used to manage graphical output displays and also user input event handling.

Classes:
GraphicsView        -- A View for graphical rendering of cellular automata.
GraphicsController  -- A Controller to pair with a GraphicsView object.
"""

import sys
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


class GraphicsView(mvc.View):
    """
    A View class implementing rendering of cellular automata with PyGame.
    
    This class handles initialization, output operation and termination of a
    PyGame instance for the express purpose of rendering cellular automata in
    the form of Model objects. This class is intended to be used with
    compatible Model and Controller objects as part of a Model-View-Controller
    deign pattern. It is recommended to use the accompanying GraphicsController
    class which handles user input from the PyGame instance.
    
    Extends:
    .mvc.View   -- Abstract Base Class for Views in the Model-View-Controller.
    
    Instance Variables:
    _canvas     -- Surface: the output display window surface.
    _closed     -- bool:    the object has been terminated.
    _colours    -- list:    the display colour scheme.
    _fullscreen -- bool:    the display is in fullscreen mode.
    _matrix     -- ndarray: the most recently provided automata state.
    _position   -- tuple:   coordinates for the top left corner of _matrix.
    _resolution -- tuple:   the (virtual) size of the display window.
    _scale      -- float:   the zoom factor in pixels/cell.
    _updates    -- bool:    flag to indicate _matrix has updates not yet
                            flushed to _canvas.
    
    Methods:
    __init__(self[, resolution][, scale][, position][,
                    colours][, fullscreen][, icon_file][, caption])
            -- Initialize class object, override View.__init__().
    close(self)
            -- Decommission, deactivate and delete the object,
               override View.close().
    move(self, distance)
            -- Move the view coordinates by a distance, Not Implemented.
    move_to(self, position)
            -- Move the view coordinates to a position, Not Implemented.
    scale(self, delta)
            -- scale the view by some delta, Not Implemented.
    scale_to(self, value)
            -- scale the view to a value, Not Implemented.
    update(self[, matrix][, flush])
            -- update and/or draw the matrix, override View.update().
    
    Warning:
    Any assignment to instance variables or calls to private methods will
    result in the object entering an illegal and potentially unrecoverable
    state.
    """
    
    def __init__(self, resolution=RESOLUTION, scale=None, position=(0, 0),
                       colours=COLOURS, fullscreen=False, icon_file=ICON_FILE,
                       caption=CAPTION):
        """
        Initialize GraphicsView object.
        
        Overrides:
        View.__init__() -- Abstract Base Class initializer.
        
        Parameters:
        self        -- GraphicsView:
                                the object itself, Required.
        resolution  -- tuple:   the resolution of the view screen,
                                Default = (1280, 720).
        scale       -- float:   the scale of the view screen in pixels/cell,
                                Default = None.
        position    -- tuple:   the starting coordinates for the top-left of
                                matrix, Default = (0, 0).
        colours     -- list:    the colour scheme for cell values,
                                Default = [(31, 1, 46), (29, 209, 166)].
        fullscreen  -- bool:    start the display in fullscreen mode,
                                Default = False.
        icon_file   -- str:     path to an image to use as window icon,
                                Default = "icon.ico".
        caption     -- str:     text to use as window caption text,
                                Default = "GraphicsView/Controller"
        
        Returns: None.
        """
        if resolution is None:
            resolution = RESOLUTION
        
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
        
        self._closed = False
    
    def update(self, matrix=None, flush=False):
        """
        Update the internal matrix and/or flush to the view screen.
        
        Overrides:
        View.update()   -- Abstract Base Class API method.
        
        This method is primarily for painting or preparing to paint the screen.
        
        Parameters:
        self    -- GraphicsView:
                            the object itself, Required.
        matrix  -- array:   the new matrix data, Default = None.
        flush   -- bool:    whether to output to view screen, Default = False.
        
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
        """
        Decommission, deactivate and delete the object permanently.
        
        This method closes the PyGame instance and sets the _closed flag to
        prevent further operations on self.
        
        Overrides:
        View.close()    -- Abstract Base Class destructor.
        
        Parameters:
        self    -- GraphicsView:    the object itself, Required.
        
        Returns None.
        """
        pygame.display.quit()
        pygame.quit()
        
        self._closed = True


class GraphicsController(mvc.Controller):
    """
    A Controller class implementing PyGame event handling on cellular automata.
    
    This class does not manage the PyGame instance but provides Controller API
    handling of PyGame events as well as the rest of the Controller API. This
    class is intended for use with a GraphicsView object providing management
    of the underlying PyGame instance. This class is intended to be used with
    compatible Model and View objects as part of a Model-View-Controller
    design pattern. It is not recommended to use this class without attaching
    a GraphicsView object as behaviour is likely to be unexpected and
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
            -- Handle PyGame events, specifically user input,
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
    state.
    """
    
    def handle_events(self):
        """
        Handle PyGame events to provide adaptability and user interactivity.
        
        This method provides proper handling of events from the PyGame event
        queue to provided canonical and extended user input and adaptability
        to window focus and resize.
        
        Parameters:
        self    -- GraphicsController:  the object itself, Required.
        
        Returns None.
        
        Exceptions Raised:
        ValueError  -- if self has already been closed with self.close().
        """
        if self._closed:
            raise ValueError("Operation on closed Controller.")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self._running = False
                elif event.key in (pygame.K_SPACE, pygame.K_p):
                    self._paused = not self._paused
                elif event.key in (pygame.K_RETURN, pygame.K_s):
                    self._step = True
                else:
                    sys.stderr.write(
                            f"{sys.argv[0]}: Unregistered key: {event.key}")
            
            elif event.type == pygame.WINDOWMINIMIZED:
                self._paused = True









################## END OF FILE ############################
