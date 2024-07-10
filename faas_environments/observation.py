from abc import ABC, abstractmethod
import numpy as np
from gymnasium import spaces

class Observation(ABC):
    def __init__(self, min_latency: int, max_latency: int, 
                 min_throughput: int, max_throughput: int, 
                 min_requests: int, max_requests: int, 
                 min_replicas: int, max_replicas: int, 
                 min_utilization: int, max_utilization: int):
        self.observation_space = None
        self.observation_space = spaces.Box(
                                    low=np.array([min_latency, min_throughput, min_requests, min_replicas, min_utilization, min_utilization]), 
                                    high=np.array([max_latency, max_throughput, max_requests, max_replicas, max_utilization, max_utilization]), 
                                    shape=(6,), 
                                    dtype=np.float64)
        
    @abstractmethod
    def set_observation_space(self,   
                 min_replicas: int, max_replicas: int, 
                 min_requests: int, max_requests: int, 
                 min_throughput: int, max_throughput: int,
                 min_latency: int, max_latency: int,
                 min_utilization: int, max_utilization: int):
        pass

    @abstractmethod
    def get_observation_space(self):
        pass

    @abstractmethod
    def get_observation(self):
        pass
