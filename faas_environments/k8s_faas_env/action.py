from .context import Context
from .defaults import defaults
from gymnasium import spaces


class Action:
    def __init__(self, ctx: Context, 
                 min_action: int = defaults.MIN_ACTION, 
                 max_action: int = defaults.MAX_ACTION):
        self.ctx = ctx
        if min_action < 0:
            raise ValueError('Minimum action value must be greater than or equal to zero.')
        if max_action < 0:
            raise ValueError('Maximum action value must be greater than or equal to zero.')
        if min_action > max_action:
            raise ValueError('Minimum action value must be less than or equal to maximum action value.')
        
        self.min_action = min_action 
        self.max_action = max_action 
        self.info = {}
        self.action_mapping = None
        self.action_space = None
        self.action_space = spaces.Discrete(max_action - min_action + 1)


    def set_action_to_scale(self):
        # Calculate the total number of actions 
        total_actions = self.max_action - self.min_action + 1
        # Calculate the start value (negative of half the range, assuming symmetric distribution)
        start_value = -(total_actions // 2)
        # Generate the mapping
        # Action is discrete and increase/decrease by value of mapping
        self.action_mapping = {action: start_value + i for i, action in enumerate(range(self.min_action, self.max_action + 1))}


    def set_action_space(self, 
                         min_action: int = defaults.MIN_ACTION, 
                         max_action: int = defaults.MAX_ACTION):
        self.action_space = spaces.Discrete(max_action - min_action + 1)
        return self.action_space
    
    def get_action_space(self):
        return self.action_space

    def get_action_mapping(self):
        if self.action_mapping is None:
            self.set_action_to_scale()
        return self.action_mapping
    
    def get_min_action(self):
        return self.action_mapping[self.min_action]
    
    def get_max_action(self):
        return self.action_mapping[self.max_action]
    
    def perform_action(self, action: int):
        if self.action_mapping is None:
            self.set_action_to_scale()
        if action not in self.action_mapping:
            raise ValueError('Invalid action value.')
        return self.action_mapping[action]