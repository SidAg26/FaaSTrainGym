import defaults as defaults
import numpy as np


class Reward:
    def __init__(self, 
                 min_reward: int = defaults.MIN_REWARD, 
                 max_reward: int = defaults.MAX_REWARD,
                 min_replicas: int = defaults.MIN_REPLICAS):
        self.reward = 0
        self.observation = None
        self.metadata = None
        self.min_reward = min_reward
        self.max_reward = max_reward
        self.min_replicas = min_replicas
        

    def _compute_reward(self, observation, metadata: dict=None):
        assert observation is not None, 'Observation cannot be empty.'
        self.observation = observation
        self.metadata = metadata
        if self.reward != 0:
            self.reward = 0

        # [average_execution, throughput, requests, replicas, cpu_utilization, memory_utilization]
        _ = observation[0] # s
        _throughput = observation[1] # %
        _ = observation[2] # int
        _replicas = observation[3] # int
        _cpu_utilization = observation[4] # % 0 - 1
        _memory_utilization = observation[5] # % 0 - 1

        if metadata is not None and 'scaled_replicas' in metadata:
            _scaled_replicas = metadata['scaled_replicas']
            
        # weight of each reward component
        _alpha = 0.75
        reward_throughput = _alpha * (_throughput ** 2)
        _beta = 0.125
        reward_cpu = _beta * (_cpu_utilization*100)
        _gamma = 0.125
        reward_memory = _gamma * (_memory_utilization*100)
        _phi = 0.25
        reward_replicas = -_phi * ((_replicas - self.min_replicas) ** 2)

        self.reward = round((reward_throughput + reward_cpu + reward_memory + reward_replicas), 2)

        # action unsuccessful or the scaled replicas is not equal to the replicas
        if (_scaled_replicas != _replicas):
            # add the minimum reward or penality
            self.reward += self.min_reward
        
        return self.reward
    
    def get_reward(self, observation, metadata):
        return self._compute_reward(observation, metadata)
    

