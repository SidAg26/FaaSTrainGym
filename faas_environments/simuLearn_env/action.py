from ..action import Action as BaseAction
from gymnasium import spaces

class Action(BaseAction):
    def __init__(self, ctx, metrics, min_action, max_action, step_size:int=128):
        super().__init__(min_action, max_action)
        self.ctx = ctx
        self.metrics = metrics
        if min_action < 0:
            raise ValueError('Minimum action value must be greater than or equal to zero.')
        if max_action < 0:
            raise ValueError('Maximum action value must be greater than or equal to zero.')
        if min_action > max_action:
            raise ValueError('Minimum action value must be less than or equal to maximum action value.')

        self.step_size = step_size    
        _actions = [i for i in range(min_action, max_action+1, step_size)]
        self.action_space = spaces.Discrete(len(_actions))

        self.action_mapping = {i: _actions[i] for i in range(len(_actions))}

    
    def set_action_to_scale(self):
        pass

    def set_action_space(self, min_action, max_action):
        _actions = [i for i in range(min_action, max_action+1, self.step_size)]
        self.action_space = spaces.Discrete(len(_actions))
        pass
        
    def set_info_metadata(self, info):
        self.info = info

    def get_info_metadata(self):
        return self.info
    
    def get_action_space(self):
        return self.action_space

    def get_action_mapping(self):
        return self.action_mapping
    
    def get_min_action(self):
        return self.min_action
    
    def get_max_action(self):
        return self.max_action
    
    def perform_action(self, action):
        return self.action_mapping[action]