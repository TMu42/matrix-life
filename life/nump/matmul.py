import numpy

from .. import mvc


rng = numpy.random.default_rng()


class GOLNumpyMatmulModel(mvc.Model):
    def __init__(self, size, density=0.5, source=None, offset=None):
        if source is not None:
            raise NotImplementedError("Matrix source not (yet) supported")
        
        self._size = size[::-1]
        
        self._init_kernels(self._size)
        
        self._mat = rng.integers(2, size=self._size, dtype=numpy.uint8)
        
        self._steps = 0
        
        self._closed = False
    
    
    def step(self, steps=1):
        if self._closed:
            raise ValueError("Operation on closed Model.")
        
        if steps < 0:
            raise NotImplementedError("Negative steps not (yet) supported")
        
        for _ in range(steps):
            self._matmul_step()
        
        self._steps += steps
    
    
    def _init_kernels(self, size):
        _lr = numpy.identity(size[1],  dtype=numpy.uint8)
        _ud = numpy.identity(size[0],  dtype=numpy.uint8)
        
        self._l_kern = numpy.roll(_lr, shift=1,  axis=1)
        self._r_kern = numpy.roll(_lr, shift=-1, axis=1)
        self._u_kern = numpy.roll(_ud, shift=1,  axis=0)
        self._d_kern = numpy.roll(_ud, shift=-1, axis=0)
    
    
    def _matmul_step(self):
        _up_down = (self._u_kern + self._d_kern)@self._mat
        _lr_corn = (self._mat + (self._u_kern + self._d_kern)@self._mat) \
                        @(self._l_kern + self._r_kern)
        
        _neighbours = _up_down + _lr_corn
        
        _generate = numpy.minimum(_neighbours//3, 1) \
                  - numpy.minimum(_neighbours//4, 1)
        
        _survive = numpy.minimum(_neighbours//2, 1) \
                 - numpy.minimum(_neighbours//4, 1)
        
        self._mat = numpy.maximum(_generate, self._mat*_survive)

########## Legacy #############################

#L = {}
#R = {}
#U = {}
#D = {}


#rng = numpy.random.default_rng()


#def new_world(width, height=None):
#    if height is None:
#        height = width
#    
#    if not width in L.keys():
#        _lr = numpy.identity(width,  dtype=numpy.uint8)
#        
#        L[width] = numpy.roll(_lr, shift=1,  axis=1)
#        R[width] = numpy.roll(_lr, shift=-1, axis=1)
#    
#    if not height in U.keys():
#        _ud = numpy.identity(height,  dtype=numpy.uint8)
#        
#        U[height] = numpy.roll(_ud, shift=1,  axis=0)
#        D[height] = numpy.roll(_ud, shift=-1, axis=0)
#    
#    return rng.integers(2, size=[height, width], dtype=numpy.uint8)


#def step(A):
#    up_down = (U[A.shape[0]] + D[A.shape[0]])@A
#    lr_corn = (A + (U[A.shape[0]] + D[A.shape[0]])@A) \
#             @(L[A.shape[1]] + R[A.shape[1]])
#    
#    neighbours = up_down + lr_corn
#    
#    generate = numpy.minimum(neighbours//3, 1) \
#             - numpy.minimum(neighbours//4, 1)
#    
#    survive = numpy.minimum(neighbours//2, 1) \
#            - numpy.minimum(neighbours//4, 1)
#    
#    return numpy.maximum(generate, A*survive)
