import numpy

from .. import mvc


rng = numpy.random.default_rng()


class GOLNumpyRollModel(mvc.Model):
    def __init__(self, size, density=0.5, source=None, offset=None):
        if source is not None:
            raise NotImplementedError("Matrix source not (yet) supported")
        self._mat = rng.integers(2, size=size, dtype=numpy.uint8)
        
        self._steps = 0
    
    
    def step(self, steps=1):
        if steps < 0:
            raise NotImplementedError("Negative steps not (yet) supported")
        
        for _ in range(steps):
            self._roll_step()
        
        self._steps += steps
    
    def close(self):
        pass
    
    def _roll_step(self):
        neighbours = numpy.roll(self._mat, ( 1,  0), (0, 1)) \
                   + numpy.roll(self._mat, (-1,  0), (0, 1)) \
                   + numpy.roll(self._mat, ( 0,  1), (0, 1)) \
                   + numpy.roll(self._mat, ( 0, -1), (0, 1)) \
                   + numpy.roll(self._mat, ( 1,  1), (0, 1)) \
                   + numpy.roll(self._mat, ( 1, -1), (0, 1)) \
                   + numpy.roll(self._mat, (-1,  1), (0, 1)) \
                   + numpy.roll(self._mat, (-1, -1), (0, 1))
        
        generate = numpy.minimum(neighbours//3, 1) \
                 - numpy.minimum(neighbours//4, 1)
        
        survive = numpy.minimum(neighbours//2, 1) \
                - numpy.minimum(neighbours//4, 1)
        
        self._mat = numpy.maximum(generate, self._mat*survive)
