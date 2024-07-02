import numpy
import scipy

from .. import mvc


KERNEL = [[2, 2, 2],
          [2, 1, 2],
          [2, 2, 2]]

rng = numpy.random.default_rng()


class GOLScipyConvolveModel(mvc.Model):
    def __init__(self, size, density=0.5, source=None, offset=None):
        if source is not None:
            raise NotImplementedError("Matrix source not (yet) supported")
        
        self._size = size[::-1]
        
        self._mat = rng.integers(2, size=self._size, dtype=numpy.uint8)
        
        self._steps = 0
        
        self._closed = False
    
    
    def step(self, steps=1):
        if self._closed:
            raise ValueError("Operation on closed Model.")
        
        if steps < 0:
            raise NotImplementedError("Negative steps not (yet) supported")
        
        for _ in range(steps):
            self._convolve_step()
        
        self._steps += steps
    
    
    def _convolve_step(self):
        _neighbours = scipy.ndimage.convolve(self._mat, KERNEL, mode="wrap")
        
        self._mat = numpy.minimum(_neighbours//5, 1) \
                  - numpy.minimum(_neighbours//8, 1)


########## Legacy #############################


#KERNEL = [[2, 2, 2],
#          [2, 1, 2],
#          [2, 2, 2]]

#rng = numpy.random.default_rng()

#def new_world(width, height=None):
#    if height is None:
#        height = width
#    
#    return rng.integers(2, size=[height, width], dtype=numpy.uint8)


#def step(A):
#    neighbours = scipy.ndimage.convolve(A, KERNEL, mode="wrap")
#    
#    new_A = numpy.minimum(neighbours//5, 1) \
#          - numpy.minimum(neighbours//8, 1)
#    
#    return new_A
