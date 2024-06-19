import numpy
import scipy


KERNEL = [[1, 1, 1],
          [1, 0, 1],
          [1, 1, 1]]

rng = numpy.random.default_rng()

def new_world(width, height=None):
    if height is None:
        height = width
    
    return rng.integers(2, size=[height, width], dtype=numpy.uint8)


def step(A):
    neighbours = scipy.ndimage.convolve(A, KERNEL, mode="wrap")
    
    generate = numpy.minimum(neighbours//3, 1) \
             - numpy.minimum(neighbours//4, 1)
    
    survive = numpy.minimum(neighbours//2, 1) \
            - numpy.minimum(neighbours//4, 1)
    
    return numpy.maximum(generate, A*survive)
