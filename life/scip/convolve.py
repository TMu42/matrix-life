"""
This module implements John Conway's Game of Life with Scipy's 2D convolution.

The Game of Life "world" is represented as a NumPy Matrix (ndarray) and global neighbour summing is performed by use of the ndimage.convolve() method from
SciPy.

Classes:
GOLScipyConvolveModel -- A Model of Game of Life using ndimage.convolve().
"""

import numpy
import scipy

from .. import mvc


KERNEL = [[2, 2, 2],
          [2, 1, 2],
          [2, 2, 2]]

rng = numpy.random.default_rng()


class GOLScipyConvolveModel(mvc.Model):
    """
    A Model class implementing Game of Life as a Matrix using scipy convolve().
    
    The Game of Life "world" is represented as a NumPy Matrix (ndarray) and
    global neighbour summing is performed via 2D convolution, provided by
    SciPy's ndimage module. This class is intended to be used with compatible
    View and Controller objects as part of a Model-View-Controller pattern.
    
    Inherits:
    ..mvc.Model -- Abstract Base Class for Models in the Model-View-Controller.
    
    Instance Variables:
    _closed -- bool:    the object has been terminated.
    _mat    -- ndarray: the state (world) matrix.
    _size   -- tuple:   the dimensions (shape) of _mat.
    _steps  -- int:     the number of iterations from initial state.
    _l_kern -- sparray: one of four diagonal arrays to assist with matmul step.
    _r_kern -- sparray: one of four diagonal arrays to assist with matmul step.
    _u_kern -- sparray: one of four diagonal arrays to assist with matmul step.
    _d_kern -- sparray: one of four diagonal arrays to assist with matmul step.
    
    Methods:
    __init__(self, size[, density][, source][, offset][, rollback])
            -- Initialize class object, override Model.__init__().
    reset(self)
            -- Reset the model to initial state, Not Implemented.
    step(self[, steps])
            -- Advance or retract the model relative, override Model.step().
    step_to(self, steps)
            -- Advance or retract the model absolute, Not Implemented.
    _init_kernels(self, size)
            -- Initialize the diagonal matrices for matmul operations, Private.
    _convolve_step(self)
            -- Advance the model one step, Private.
    
    Inherits:
    close(self)
            -- Decommission, deactivate and delete the object.
    
    Warning:
    Any assignment to instance variables or calls to private methods will
    result in the object entering an illegal and potentially unrecoverable
    state.
    """
    
    def __init__(self, size, density=0.5, source=None, offset=None,
                             rollback=0):
        """
        Initialize GOLScipyConvolveModel object.
        
        Overrides:
        Model.__init__()    -- Abstract Base Class initializer.
        
        Parameters:
        self        -- GOLScipyConvolveModel:
                                the object itself, Required.
        size        -- tuple:   the dimensions (shape) of the "world",
                                Required.
        density     -- float:   the initial statistical density of living
                                cells, Default = 0.5, Ignored.
        source      -- string:  a file name to initialize the "world", Not
                                Implemented.
        offset      -- tuple:   the offset coordinates for source, Ignored.
        rollback    -- int:     the requested rollback memory for back-steps,
                                Ignored.
        
        Returns: None.
        
        Exceptions Raised:
        NotImplementedError -- if source is provided.
        """
        if source is not None:
            raise NotImplementedError("Matrix source not (yet) supported")
        
        self._size = size[::-1]
        
        self._mat = rng.integers(2, size=self._size, dtype=numpy.uint8)
        
        self._steps = 0
        
        self._closed = False
    
    
    def step(self, steps=1):
        """
        Advance or retract the model some number of steps.
        
        Overrides:
        Model.step()    -- Abstract Base Class API method.
        
        Parameters:
        self    -- GOLScipyConvolveModel:
                        the object itself, Required.
        steps   -- int: the number of steps to advance or retract if negative,
                        Default = 1.
        
        Returns: None.
        
        Exceptions Raised:
        ValueError          -- if self has already been closed with
                               self.close().
        NotImplementedError -- if steps is negative.
        """
        if self._closed:
            raise ValueError("Operation on closed Model.")
        
        if steps < 0:
            raise NotImplementedError("Negative steps not (yet) supported")
        
        for _ in range(steps):
            self._convolve_step()
        
        self._steps += steps
    
    
    def _convolve_step(self):
        """
        Advance the model one step using the scipy convolution algorithm.
        
        Neighbour and identity relations are found by 2D convolution of the
        "world" matrix with a constant 3x3 kernel matrix. The kernel is
        designed to provide strict threshold values for life in the next
        iteration, this being determined using integer division thresholding.
        
        Parameters:
        self    -- GOLScipyConvolveModel:
                        the object itself, Required.
        
        Returns: None.
        
        Note:
        This is a private "helper" method, externally this operation should be
        performed by a call to step() with the default value of 1 for steps.
        External calls to this method may leave the object in an illegal,
        unrecoverable state.
        """
        _neighbours = scipy.ndimage.convolve(self._mat, KERNEL, mode="wrap")
        
        self._mat = numpy.minimum(_neighbours//5, 1) \
                  - numpy.minimum(_neighbours//8, 1)
