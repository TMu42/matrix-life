import numpy
import scipy

from .. import mvc


class GOLScipyConvolveModel(mvc.Model):
    pass


########## Legacy #############################


KERNEL = [[2, 2, 2],
          [2, 1, 2],
          [2, 2, 2]]

rng = numpy.random.default_rng()

def new_world(width, height=None):
    if height is None:
        height = width
    
    return rng.integers(2, size=[height, width], dtype=numpy.uint8)


def step(A):
    neighbours = scipy.ndimage.convolve(A, KERNEL, mode="wrap")
    
    new_A = numpy.minimum(neighbours//5, 1) \
          - numpy.minimum(neighbours//8, 1)
    
    return new_A
