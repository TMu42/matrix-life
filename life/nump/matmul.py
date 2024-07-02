import numpy

from .. import mvc


class GOLNumpyMatmulModel(mvc.Model):
    pass


########## Legacy #############################

L = {}
R = {}
U = {}
D = {}


rng = numpy.random.default_rng()


def new_world(width, height=None):
    if height is None:
        height = width
    
    if not width in L.keys():
        _lr = numpy.identity(width,  dtype=numpy.uint8)
        
        L[width] = numpy.roll(_lr, shift=1,  axis=1)
        R[width] = numpy.roll(_lr, shift=-1, axis=1)
    
    if not height in U.keys():
        _ud = numpy.identity(height,  dtype=numpy.uint8)
        
        U[height] = numpy.roll(_ud, shift=1,  axis=0)
        D[height] = numpy.roll(_ud, shift=-1, axis=0)
    
    return rng.integers(2, size=[height, width], dtype=numpy.uint8)


def step(A):
    up_down = (U[A.shape[0]] + D[A.shape[0]])@A
    lr_corn = (A + (U[A.shape[0]] + D[A.shape[0]])@A) \
             @(L[A.shape[1]] + R[A.shape[1]])
    
    neighbours = up_down + lr_corn
    
    generate = numpy.minimum(neighbours//3, 1) \
             - numpy.minimum(neighbours//4, 1)
    
    survive = numpy.minimum(neighbours//2, 1) \
            - numpy.minimum(neighbours//4, 1)
    
    return numpy.maximum(generate, A*survive)
