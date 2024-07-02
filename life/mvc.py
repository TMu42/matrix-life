import time


class Model:
    def __init__(self, size, density=None, source=None, offset=None,
                             rollback=0, **kwargs):
        raise NotImplementedError
    
    def step(self, steps=1):
        raise NotImplementedError
    
    def step_to(self, steps):
        raise NotImplementedError
    
    def reset(self):
        raise NotImplementedError
    
    def close(self):
        self._closed = True


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
        self._closed = True


class Controller:
    def __init__(self, model=None, view=None, delay=0.01, **kwargs):
        if type(self) is Controller:
            raise NotImplementedError
        else:
            self._model = model
            self._view  = view
            
            self._delay = delay
            
            self._running = True
            self._paused  = False
            self._closed  = False
    
    def connect_model(self, model):
        if self._closed:
            raise ValueError("Operation on closed Controller.")
        
        self._model = model
    
    def connect_view(self, model):
        if self._closed:
            raise ValueError("Operation on closed Controller.")
        
        self._view = view
    
    def handle_events(self):
        raise NotImplementedError
    
    def run(self):
        if self._closed:
            raise ValueError("Operation on closed Controller.")
        
        try:
            while self._running:
                self.handle_events()
                
                if not self._paused:
                    time.sleep(self._delay)
                else:
                    time.sleep(0.01)
        except KeyboardInterrupt:
            pass
        except BaseException:
            self.close()
            
            raise
        else:
            self.close()
    
    def close(self):
        if self._model is not None:
            self._model.close()
        
        if self._view is not None:
            self._view.close()
        
        self._closed = True
