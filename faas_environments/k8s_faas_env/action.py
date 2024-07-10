from .context import Context
from .metrics_collection import MetricsCollection
import defaults as defaults
from gymnasium import spaces


class Action:
    def __init__(self, ctx: Context, metrics: MetricsCollection,
                 min_action: int = defaults.MIN_ACTION, 
                 max_action: int = defaults.MAX_ACTION,
                 min_replicas: int = defaults.MIN_REPLICAS,
                 max_replicas: int = defaults.MAX_REPLICAS):
        self.ctx = ctx
        self.metrics = metrics
        if min_action < 0:
            raise ValueError('Minimum action value must be greater than or equal to zero.')
        if max_action < 0:
            raise ValueError('Maximum action value must be greater than or equal to zero.')
        if min_action > max_action:
            raise ValueError('Minimum action value must be less than or equal to maximum action value.')
        if min_replicas < 0:
            raise ValueError('Minimum replicas value must be greater than or equal to zero.')
        if max_replicas < 0:
            raise ValueError('Maximum replicas value must be greater than or equal to zero.')
        if min_replicas > max_replicas:
            raise ValueError('Minimum replicas value must be less than or equal to maximum replicas value.')
        
        self.min_action = min_action 
        self.max_action = max_action 
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self._k8s_scale_api = self.ctx.get_k8s_scale_api()
        self._k8s_deployment_name = self.ctx.get_k8s_deployment_name()
        self._k8s_deployment_namespace = self.ctx.get_k8s_deployment_namespace()
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
    
    def set_info_metadata(self, info: dict):
        self.info = info

    def get_info_metadata(self):
        return self.info

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
        try:
            # number of ready function replicas 
            ready_replicas = self._k8s_scale_api.read_namespaced_deployment(
                                                        name=self._k8s_deployment_name,
                                                        namespace=self._k8s_deployment_namespace).status.ready_replicas
            if ready_replicas == None:
                ready_replicas = 0
                print('No ready pods found')
        except Exception as e:
            print('Error in reading ready pods')
            ready_replicas = 0

        scaled_replicas = ready_replicas + self.action_mapping[action]
        scaling_feedback = False

        if self.action_mapping[action] < 0:
            if (scaled_replicas >= defaults.MIN_REPLICAS):
                scaling_feedback = True
                body = {'spec': {'replicas': scaled_replicas}}
                try:
                    _ = self._k8s_scale_api.patch_namespaced_deployment_scale(
                                                        name=self._k8s_deployment_name, 
                                                        namespace=self._k8s_deployment_namespace,
                                                        body=body).spec.replicas
                except Exception as _:
                    print('Error in scaling down')
                    scaling_feedback = False
                    
            else:
                print('Cannot scale below minimum replicas')
                scaling_feedback = False

        elif self.action_mapping[action] == 0:
            if scaled_replicas == 0:
                print('No pods to scale')
                scaling_feedback = False
            else:
                print('No scaling required')
                scaling_feedback = True
        
        else:
            if (self.min_replicas <= scaled_replicas <= self.max_replicas):
                scaling_feedback = True
                body = {'spec': {'replicas': scaled_replicas}}
                try:
                    _ = self._k8s_scale_api.patch_namespaced_deployment_scale(
                                                        name=self._k8s_deployment_name, 
                                                        namespace=self._k8s_deployment_namespace,
                                                        body=body).spec.replicas
                except Exception as _:
                    print('Error in scaling up')
                    scaling_feedback = False
                    
            else:
                print('Cannot scale above maximum replicas')
                scaling_feedback = False
        _info = {'action': self.action_mapping[action], 
                 'scaling_feedback': scaling_feedback,
                 'pre_scaled_replicas': ready_replicas,
                 'scaled_replicas': scaled_replicas
                }
        self.set_info_metadata(_info) # just to store the info
        return _info