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
        _input = len(self.ctx.get_unique_input()) # number of unique input values
        _memory_list = len(self.ctx.get_unique_memory()) # number of unique memory values
        _, _duration = self.ctx.get_execution_time_range() # min and max execution time
        _status = len(defaults.STATUS) # number of status values
        self.observation_space = spaces.MultiDiscrete([_memory_list, _input, _duration, _status])

    
    def set_observation_space(self, min_latency: int, max_latency: int, 
                    min_throughput: int, max_throughput: int, 
                    min_requests: int, max_requests: int, 
                    min_replicas: int, max_replicas: int, 
                    min_utilization: int, max_utilization: int):
        pass
        
    def _set_observation(self, observation):
        self.observation = observation

    def get_observation_space(self):
        return self.observation_space
    
    @singledispatch
    def get_observation(self):
        return self.observation
    
    @singledispatch
    def get_observation(self, input:int, memory:int):
        _df = self.ctx.get_dataframe_at_memory_input(memory, input)
        self.observation = _df['Memory', 'Input', 'Duration', 'Status']
        return self.observation

    
