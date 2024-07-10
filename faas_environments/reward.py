from abc import ABC, abstractmethod


class Reward(ABC):
    def __init__(self, min_reward: int, max_reward: int):
        self.reward = 0
        self.observation = None
        self.metadata = None
        self.min_reward = min_reward
        self.max_reward = max_reward

    @abstractmethod
    def _compute_reward(self, observation, metadata: dict = None):
        pass

    @abstractmethod
    def get_reward(self, observation, metadata: dict = None):
        pass