import time as time
import gymnasium as gym
import defaults as defaults
from .context import Context 
from .observation import Observation
from .action import Action
from .reward import Reward
from .metrics_collection import MetricsCollection

class Environment(gym.Env):
    # This is an example of a custom environment for OpenFaaS on Kubernetes for
    # the FaaSTrainGym_v1 library. The environment is based on the OpenAI Gym/Gymnasium
    # interface. The environment is designed to be used with Function Scaling APIs and RL
    # algorithms for scaling functions in a Kubernetes cluster.


    # every environment should support None render mode
    metadata = {'render_modes': ['human', 'tensorflow', None]}

    def __init__(self, ctx:Context | None, 
                 func_cpu: int = defaults.FUNCTION_CPU_REQUEST, 
                 func_mem: int = defaults.FUNCTION_MEMORY_REQUEST,
                 min_action: int = defaults.MIN_ACTION,
                 max_action: int = defaults.MAX_ACTION, 
                 min_reward: int = defaults.MIN_REWARD,
                 max_reward: int = defaults.MAX_REWARD,
                 min_replicas: int = defaults.MIN_REPLICAS,
                 max_replicas: int = defaults.MAX_REPLICAS,
                 sample_interval: int = defaults.SAMPLING_INTERVAL,
                 episodes: int = defaults.EPISODES,
                 render_mode=None) -> None:
        super(Environment, self).__init__()

        # TODO Step1: Context object for Kubernetes and Prometheus API
        if ctx is None:
            ctx = Context()
        self.ctx = ctx
        self.sample_interval = sample_interval
        self.metrics = MetricsCollection(ctx=self.ctx, sampling_window=self.sample_interval)
        
        # TODO Step2: Define the Observation object
        # [avg_execution, throughput, requests, replicas, avg_cpu/req, avg_mem/req]
        self._observation = Observation(ctx=self.ctx, metrics=self.metrics)
        # self.observation_space = self._observation.get_observation_space()

        # TODO Step3: Define the function CPU and Memory requests
        self.func_cpu = func_cpu 
        self.func_mem = round(func_mem / 1024, 2) # converting to Gi
        
        # TODO Step4: Check the render mode for logging
        assert render_mode in self.metadata['render_modes'], f"Invalid render mode {render_mode}"
        self.render_mode = render_mode
        if self.render_mode == 'tensorflow':
            model_name = 'model-OpenFaaS-Scaling-RL'
            # TODO - initialise tensorboard
            # to be done in the render method

        # TODO Step5: Define the Action object
        self._action = Action(ctx=self.ctx, metrics=self.metrics, 
                              min_action=min_action, max_action=max_action,
                              min_replicas=min_replicas, max_replicas=max_replicas)
        # self.action_space = self._action.get_action_space()
        
        # TODO Step6: Define the Reward object
        self._reward = Reward(min_reward=min_reward,
                              max_reward=max_reward)

        # TODO Step6: Configurable Environment Parameters
        self._terminal = episodes
        self._timestep = 0
        self._episode = 0
        self._last_obs = None
        
 
    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        # reset other paramters based on the environment
        self._info = self._action.get_info_metadata()
        self._last_obs = self._observation.get_observation()
        self._done = False
        self._timestep = 0
      
        return self._last_obs, self.info


    def step(self, action):
        # Perform the action and get the feedback
        self._info = self._action.perform_action(action)
       
        # Wait for the action to be completed and get the next observation
        time.sleep(self.sample_interval)
        self._timestep += 1

        # get the next observation after the action
        next_observation = self._observation.get_observation()
        # calculate reward
        reward = self._reward.get_reward(next_observation, self._info)

        # check for episode termination
        if self._timestep >= self._terminal:
            self._done = True
            self._episode += 1

        if self.render_mode == 'tensorflow':
            print("Tensorflow logging")
            self.render(mode='tensorflow')
            # TODO - write to tensorboard
            # episodic reward calculation and logging
                       
        # observation, reward, terminated(done), truncated(max_timestep), info
        return next_observation, reward, self._done, False, self._info
    
    
    def render(self, mode='human', close=False):
        # render or print information on screen or add to the tensorboard, etc.
        pass

    def close(self):
        # close any open resources
        pass