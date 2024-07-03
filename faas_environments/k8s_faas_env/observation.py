import numpy as np
from gymnasium import spaces


class Observation:
    def __init__(self, **kwargs):
        _dict_keys = kwargs.keys()
        for key in _dict_keys:
            setattr(self, key, kwargs[key])
        
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(2,), dtype=np.float32)
        

    def __str__(self):
        return f"Observation(resources={self.resources}, containers={self.containers})"

    def __repr__(self):
        return str(self)