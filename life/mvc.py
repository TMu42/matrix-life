import time


class Model:
    def __init__(self, size, density=None, source=None, offset=None, **kwargs):
        raise NotImplementedError
    
    def step(self, steps=1):
        raise NotImplementedError
    
    def step_to(self, steps):
        raise NotImplementedError
    
    def reset(self):
        raise NotImplementedError
    
    def close(self):
        raise NotImplementedError


class View:
    def __init__(self, resolution=None, scale=None, position=None,
                       colours=None, **kwargs):
        raise NotImplementedError
    
    def update(self, matrix=None, flush=False):
        raise NotImplementedError
    
    def move(self, distance):
        raise NotImplementedError
    
    def move_to(self, position):
        raise NotImplementedError
    
    def scale(self, delta):
        raise NotImplementedError
    
    def scale_to(self, value):
        raise NotImplementedError
    
    def close(self):
        raise NotImplementedError


# Not sure if this abstract base class is needed but might be useful...
class Controller:
    def __init__(self, model=None, view=None, **kwargs):
        raise NotImplementedError
    
    def connect_model(self, model):
        self._model = model
    
    def connect_view(self, model):
        self._view = view
    
    def handle_events(self):
        raise NotImplementedError
    
    def run(self):
        while self._running:
            self.handle_events()
            
            if not self._paused:
                time.sleep(self._delay)
            else:
                time.sleep(0.01)
    
    def close(self):
        raise NotImplementedError
