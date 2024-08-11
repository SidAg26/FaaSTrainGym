import time as time
import gymnasium as gym
from .context import Context 
from .observation import Observation
from .action import Action




class SimuEnv(gym.Env):
    def __init__(self, file_path:str=None, step_size:int=128) -> None:
        super().__init__()
        self.ctx = Context(file_path=file_path, step_size=step_size)
        self.ctx.load_file()

        _observation = Observation(ctx=self.ctx, step_size=step_size)
        self.observation_space = _observation.get_observation_space()



