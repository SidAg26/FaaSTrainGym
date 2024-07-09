import numpy as np
from .context import Context
from .defaults import defaults
from gymnasium import spaces


class Observation:
    def __init__(self, ctx: Context, 
                 min_replicas: int = defaults.MIN_REPLICAS, 
                 max_replicas: int = defaults.MAX_REPLICAS, 
                 min_requests: int = defaults.MIN_REQUESTS,
                 max_requests: int = defaults.MAX_REQUESTS, 
                 min_throughput: int = defaults.MIN_THROUGHPUT,
                 max_throughput: int = defaults.MAX_THROUGHPUT,
                 min_latency: int = defaults.MIN_LATENCY,
                 max_latency: int = defaults.MAX_LATENCY,
                 min_utilization: int = defaults.MIN_UTILIZATION,
                 max_utilization: int = defaults.MAX_UTILIZATION):

        self.ctx = ctx # Context object
        self.observation_space = None
        self.observation_space = spaces.Box(
                                    low=np.array([min_latency, min_throughput, min_requests, min_replicas, min_utilization, min_utilization]), 
                                    high=np.array([max_latency, max_throughput, max_requests, max_replicas, max_utilization, max_utilization]), 
                                    shape=(6,), 
                                    dtype=np.float64)   

    def set_observation_space(self,   
                 min_replicas: int = defaults.MIN_REPLICA, 
                 max_replicas: int = defaults.MAX_REPLICAS, 
                 min_requests: int = defaults.MIN_REQUESTS,
                 max_requests: int = defaults.MAX_REQUESTS, 
                 min_throughput: int = defaults.MIN_THROUGHPUT,
                 max_throughput: int = defaults.MAX_THROUGHPUT,
                 min_latency: int = defaults.MIN_LATENCY,
                 max_latency: int = defaults.MAX_LATENCY,
                 min_utilization: int = defaults.MIN_UTILIZATION,
                 max_utilization: int = defaults.MAX_UTILIZATION):
        
        self.observation_space = spaces.Box(
                            low=np.array([min_latency, min_throughput, min_requests, min_replicas, min_utilization, min_utilization]), 
                            high=np.array([max_latency, max_throughput, max_requests, max_replicas, max_utilization, max_utilization]), 
                            shape=(6,), 
                            dtype=np.float64) 
        return self.observation_space

    def get_observation_space(self):
        return self.observation_space
    
    def get_observation(self):
        # Get the current latency, throughput, requests, replicas, CPU utilization, and memory utilization
        latency = self.ctx.get_prometheus_api().get_latency()
        throughput = self.ctx.get_prometheus_api().get_throughput()
        requests = self.ctx.get_prometheus_api().get_requests()
        replicas = self.ctx.get_prometheus_api().get_replicas()
        cpu_utilization = self.ctx.get_prometheus_api().get_cpu_utilization()
        memory_utilization = self.ctx.get_prometheus_api().get_memory_utilization()
        return np.array([latency, throughput, requests, replicas, cpu_utilization, memory_utilization])