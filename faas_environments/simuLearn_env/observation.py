import numpy as np
from functools import singledispatch
from ..observation import Observation as BaseObservation
from . import defaults as defaults
from .context import Context
from gymnasium import spaces



class Observation(BaseObservation):
    def __init__(self, ctx:Context, step_size:int=128):
        super().__init__(0,0,0,0,0,0,0,0,0,0)
        self.ctx = ctx
        self.step_size = step_size
        self.observation = None
        # Memory, Input, Duration, Status
        _input = len([i for i in range(10, 10000, 100)])
        self.observation_space = spaces.MultiDiscrete([24, _input, ])

    
    def set_observation_space(self, min_latency: int, max_latency: int, 
                    min_throughput: int, max_throughput: int, 
                    min_requests: int, max_requests: int, 
                    min_replicas: int, max_replicas: int, 
                    min_utilization: int, max_utilization: int):
        pass

    def get_observation_space(self):
        return self.observation_space
    
    @singledispatch
    def get_observation(self):
        return self.observation
    
    def _set_observation(self, observation):
        self.observation = observation
    
    @singledispatch
    def get_observation(self, input:int, memory:int):
        _df = self.ctx.get_dataframe_at_memory_input(memory, input)
        self.observation = _df['Memory', 'Input', 'Duration', 'Status']
        return self.observation

    
