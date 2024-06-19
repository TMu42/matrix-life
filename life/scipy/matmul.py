import numpy
import scipy


L = {}
R = {}
U = {}
D = {}


rng = numpy.random.default_rng()


def new_world(width, height=None):
    if height is None:
        height = width
    
    if not width in L.keys():
        L[width] = scipy.sparse.diags_array([[1], (width - 1)*[1]],
                                                    offsets=[1-width, 1])
        R[width] = scipy.sparse.diags_array([[1], (width - 1)*[1]],
                                                    offsets=[width-1, -1])
    
    if not height in U.keys():
        U[height] = scipy.sparse.diags_array([[1], (height - 1)*[1]],
                                                    offsets=[1-height,  1])
        D[height] = scipy.sparse.diags_array([[1], (height - 1)*[1]],
                                                    offsets=[height-1, -1])
    
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
