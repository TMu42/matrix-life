"""
Abstract Base Classes (ABCs) for Model-View-Controllers for cellular automata.

Classes:
Model       -- ABC for cellular automaton Models.
View        -- ABC for cellular automaton Views.
Controller  -- ABC for cellular automaton Controllers.
"""

import time


class Model:
    """
    Base class for all cellular automaton Models providing a common interface.
    
    Instance Variables:
    _closed -- bool:    the object has been terminated.
    
    Methods:
    __init__(self, size[, density][, source][, offset][, rollback][, **kwargs])
            -- Initialize class object, Abstract.
    close(self)
            -- Decommission, deactivate and delete the object.
    reset(self)
            -- Rest the model, Abstract.
    step(self[, steps])
            -- Advance or retract the model relative, Abstract.
    step_to(self, steps)
            -- Advance or retract the model absolute, Abstract.
    
    Note:
    Classes implementing/extending Model should raise ValueError if public
    methods are called after close() has been called (i.e. _closed == True).
    This will ensure that assumptions about validity are not violated.
    """
    
    def __init__(self, size, density=None, source=None, offset=None,
                             rollback=0, **kwargs):
        """
        Initializer for Model objects, Abstract.
        
        Parameters:
        self        -- Model:   the object itself, Required.
        size        -- tuple:   the dimensions (shape) of the "world",
                                Required.
        density     -- float:   the initial statistical density of living
                                cells, Default = 0.5.
        source      -- string:  a file name to initialize the "world",
                                Default = None.
        offset      -- tuple:   the offset coordinates for source,
                                Default = None.
        rollback    -- int:     the requested rollback memory for back-steps,
                                Default = 0.
        
        Returns: None.
        
        Exceptions Raised
        NotImplementedError -- always
        """
        raise NotImplementedError
    
    def step(self, steps=1):
        """
        Advance or retract the model some number of steps, Abstract.
        
        Parameters:
        self    -- Model:   the object itself, Required.
        steps   -- int:     the number of steps to advance or retract if
                            negative, Default = 1.
        
        Returns: None.
        
        Exceptions Raised:
        NotImplementedError -- always.
        """
        raise NotImplementedError
    
    def step_to(self, steps):
        """
        Advance or retract the model to some point, Abstract.
        
        Parameters:
        self    -- Model:   the object itself, Required.
        steps   -- int:     the point to advance or retract to, Required.
        
        Returns: None.
        
        Exceptions Raised:
        NotImplementedError -- always.
        """
        raise NotImplementedError
    
    def reset(self):
        """
        Reset the model to its initial state, Abstract.
        
        Parameters:
        self    -- Model:   the object itself, Required.
        
        Returns None.
        
        Exceptions Raised:
        NotImplementedError -- always.
        """
        raise NotImplementedError
    
    def close(self):
        """
        Decommission, deactivate and delete the object permanently.
        
        This is the only non-abstract method in this class and provides basic
        decommissioning however subclasses implementing this may need to
        override or extend this to ensure that memory and state are managed
        and respected cleanly.
        
        Parameters:
        self    -- Model:   the object itself, Required.
        
        Returns None.
        """
        self._closed = True


class View:
    """
    Base class for all cellular automaton Views providing a common interface.
    
    Instance Variables:
    _closed -- bool:    the object has been terminated.
    
    Methods:
    __init__(self[, resolution][, scale][, position][, colours][, **kwargs])
            -- Initialize class object, Abstract.
    close(self)
            -- Decommission, deactivate and delete the object.
    move(self, distance)
            -- Move the view coordinates by a distance, Abstract.
    move_to(self, position)
            -- Move the view coordinates to a position, Abstract.
    scale(self, delta)
            -- scale the view by some delta, Abstract.
    scale_to(self, value)
            -- scale the view to a value, Abstract.
    update(self[, matrix][, flush])
            -- update and or draw the matrix, Abstract.
    
    Note:
    Classes implementing/extending View should raise ValueError if public
    methods are called after close() has been called (i.e. _closed == True).
    This will ensure that assumptions about validity are not violated.
    """
    
    def __init__(self, resolution=None, scale=None, position=None,
                       colours=None, **kwargs):
        """
        Initializer for View objects, Abstract.
        
        Parameters:
        self        -- View:    the object itself, Required.
        resolution  -- tuple:   the resolution of the view screen,
                                Default = None.
        scale       -- float:   the scale of the view screen in pixels/cell,
                                Default = None.
        position    -- tuple:   the starting coordinates for the top-left of
                                matrix, Default = None.
        colours     -- list:    the colour scheme for cell values,
                                Default = None.
        **kwargs    -- dict:    catch any additional arguments provided by
                                subclasses if they should go through to the
                                keeper.
        
        Returns: None.
        
        Exceptions Raised
        NotImplementedError -- always
        """
        raise NotImplementedError
    
    def update(self, matrix=None, flush=False):
        """
        Update the internal matrix and/or flush to the view screen, Abstract.
        
        This method is primarily for painting or preparing to paint the screen.
        
        Parameters:
        self    -- Model:   the object itself, Required.
        matrix  -- array:   the new matrix data, Default = None.
        flush   -- bool:    whether to output to view screen, Default = False.
        
        Returns None.
        
        Exceptions Raised:
        NotImplementedError -- always.
        """
        raise NotImplementedError
    
    def move(self, distance):
        """
        Move the view coordinates by a relative amount or distance, Abstract.
        
        This method adjusts the View object's internal position value and is
        primarily useful for panning on automata which are larger than the
        screen resolution.
        
        Parameters:
        self        -- Model:   the object itself, Required.
        distance    -- tuple:   the x, y distance to move, Required.
        
        Returns None.
        
        Exceptions Raised:
        NotImplementedError -- always.
        """
        raise NotImplementedError
    
    def move_to(self, position):
        """
        Move the view coordinates to an absolute position, Abstract.
        
        This method adjusts the View object's internal position value and is
        primarily useful for panning on automata which are larger than the
        screen resolution.
        
        Parameters:
        self        -- Model:   the object itself, Required.
        position    -- tuple:   the x, y coordinates to move to, Required.
        
        Returns None.
        
        Exceptions Raised:
        NotImplementedError -- always.
        """
        raise NotImplementedError
    
    def scale(self, delta):
        """
        Change the scale (zoom) of the display by some amount, Abstract.
        
        This method adjusts the View object's internal scale value by some
        proportion, posibly with rounding and is useful for zooming in and out
        on large automata.
        
        Parameters:
        self    -- Model:   the object itself, Required.
        delta   -- float:   the relative scale (zoom) factor.
        
        Returns None.
        
        Exceptions Raised:
        NotImplementedError -- always.
        """
        raise NotImplementedError
    
    def scale_to(self, value):
        """
        Change the scale (zoom) of the display to some value, Abstract.
        
        This method adjusts the View object's internal scale value and is
        useful for zooming in and out on large automata.
        
        Parameters:
        self    -- Model:   the object itself, Required.
        value   -- float:   the absolute scale (zoom) factor.
        
        Returns None.
        
        Exceptions Raised:
        NotImplementedError -- always.
        """
        raise NotImplementedError
    
    def close(self):
        """
        Decommission, deactivate and delete the object permanently.
        
        This is the only non-abstract method in this class and provides basic
        decommissioning however subclasses implementing this may need to
        override or extend this to ensure that memory and state are managed
        and respected cleanly.
        
        Parameters:
        self    -- Model:   the object itself, Required.
        
        Returns None.
        """
        self._closed = True


class Controller:
    """
    Base class for cellular automaton Controllers providing a common interface.
    
    Instance Variables:
    _model      -- Model:   the Model object to run.
    _view       -- View:    the View object to update and adjust.
    _delay      -- float:   additional delay in seconds added to each loop.
    _running    -- bool:    the automaton is not finished.
    _paused     -- bool:    the automaton is paused.
    _closed     -- bool:    the object has been terminated.
    
    Methods:
    __init__(self[, model][, view][, delay][, paused][, **kwargs])
            -- Initialize class object.
    close(self)
            -- Decommission, deactivate and delete the object.
    connect_model(self, model)
            -- Connect a Model object to the Controller.
    connect_view(self, view)
            -- Connect a View object to the Controller.
    handle_events(self)
            -- Handle interface specific events (e.g. user input).
    run(self)
            -- Run the main control loop.
    
    Note:
    Classes implementing/extending Controller should raise ValueError if public
    methods are called after close() has been called (i.e. _closed == True).
    This will ensure that assumptions about validity are not violated.
    """
    
    def __init__(self, model=None, view=None, delay=0.01,
                       paused=False, **kwargs):
        """
        Initializer for Controller objects.
        
        Parameters:
        self        -- Controller:  the object itself, Required.
        model       -- Model:       the Model to control and run,
                                    Default = None.
        view        -- View:        the View to manage and update,
                                    Default = None.
        delay       -- float:       the additional delay in seconds per cycle,
                                    Default = 0.01.
        paused      -- bool:        Start the simulation in paused state.
        **kwargs    -- int:         catch any additional arguments provided by
                                    subclasses if they should go through to the
                                    keeper.
        
        Returns: None.
        
        Exceptions Raised
        NotImplementedError -- if called on the Base Class, Controller is
                               Abstract however the initializer can be safely
                               inherited.
        """
        if type(self) is Controller:
            raise NotImplementedError
        else:
            self._model = model
            self._view  = view
            
            self._delay = delay
            
            self._running = True
            self._paused  = paused
            self._closed  = False
    
    def connect_model(self, model):
        """
        Connect a Model object to this Controller.
        
        This method can be used if no Model was provided at initialization or
        if a new Model is desired to replace the original.
        
        Parameters:
        self    -- Controller:  the object itself, Required.
        model   -- Model:       the model to attach, Required.
        
        Returns None.
        
        Exceptions Raised:
        ValueError  --  if self has already been closed with self.close().
        """
        if self._closed:
            raise ValueError("Operation on closed Controller.")
        
        self._model = model
    
    def connect_view(self, view):
        """
        Connect a View object to this Controller.
        
        This method can be used if no View was provided at initialization or
        if a new View is desired to replace the original.
        
        Parameters:
        self    -- Controller:  the object itself, Required.
        view    -- View:        the view to attach, Required.
        
        Returns None.
        
        Exceptions Raised:
        ValueError  --  if self has already been closed with self.close().
        """
        if self._closed:
            raise ValueError("Operation on closed Controller.")
        
        self._view = view
    
    def handle_events(self):
        """
        Handle all async i/o events related to this Controller, Abstract.
        
        This method should be overridden to provide event queue handling for
        user input or any other asynchronous events which apply to the
        Controller.
        
        Parameters:
        self    -- Controller:  the object itself, Required.
        
        Returns None.
        
        Exceptions Raised:
        NotImplementedError -- always.
        """
        raise NotImplementedError
    
    def run(self):
        """
        Run the main control loop.
        
        This method sequentially and iteratively updates the Model, updates
        the View and calls its own event handler. It loops until the
        self._running flag flips to False (usually due to some event) and then
        calls self.close() on itself. It also calls self.close() if it
        encounters KeyboardInterrupt or any other Exception before re-raising
        in the latter case and so fails gracefully allowing any cleanup to
        occur.
        
        Parameters:
        self    -- Controller:  the object itself, Required.
        
        Returns None.
        
        Exceptions Raised:
        ValueError  --  if self has already been closed with self.close().
        """
        if self._closed:
            raise ValueError("Operation on closed Controller.")
        
        try:
            while self._running:
                self.handle_events()
                
                if self._model is not None and self._running \
                        and (not self._paused or self._model._steps == 0):
                    self._model.step()
                    
                    if self._view is not None:
                        self._view.update(self._model._mat, True)
                
                if not self._paused:
                    time.sleep(self._delay)
                else:
                    time.sleep(0.01)
        except KeyboardInterrupt:
            self.close()
        except BaseException:
            self.close()
            
            raise
        else:
            self.close()
    
    def close(self):
        """
        Decommission, deactivate and delete the object permanently.
        
        Closing Controller calls the close() methods of the attached Model and
        View objects (if any) before executing its own basic decommission.
        Subclasses implementing this should extend this method rather than 
        overriding it to ensure that Models and Views are appropriately
        decommissioned. If a Model or View needs to be preserved (perhaps to
        attach to annother Controller), connect_model(None) or 
        connect_view(None) should be called before close() (of course ensuring
        that the Model or View has been assigned elsewhere first). It is likely
        that implementing classes will need to extend this to ensure that
        memory and state are managed and respected cleanly.
        
        Parameters:
        self    -- Model:   the object itself, Required.
        
        Returns None.
        """
        if self._model is not None:
            self._model.close()
        
        if self._view is not None:
            self._view.close()
        
        self._closed = True
