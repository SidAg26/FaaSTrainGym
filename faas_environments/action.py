from abc import ABC, abstractmethod
from gymnasium import spaces

class Action(ABC):
    def __init__(self, min_action: int, max_action: int):
        self.min_action = min_action
        self.max_action = max_action
        self.action_mapping = None
        self.action_space = None
        self.action_space = spaces.Discrete(max_action - min_action + 1)
    
    @abstractmethod
    def set_action_to_scale(self):
        pass
    
    @abstractmethod
    def set_action_space(self, min_action: int, max_action: int):
        pass
    
    @abstractmethod
    def set_info_metadata(self, info: dict):
        pass
    
    @abstractmethod
    def get_info_metadata(self):
        pass

    @abstractmethod
    def get_action_space(self):
        pass

    @abstractmethod
    def get_action_mapping(self):
        pass

    @abstractmethod
    def get_min_action(self):
        pass

    @abstractmethod
    def get_max_action(self):
        pass

    @abstractmethod
    def perform_action(self, action: int):
        pass