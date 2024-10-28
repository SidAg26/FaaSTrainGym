import os

# Default values for the environment
MIN_REPLICAS = 1 # minimum number of replicas
MAX_REPLICAS = 10 # maximum number of replicas
MIN_CPU = 0.1 # 100m
MAX_CPU = 1 # 1000m
MIN_MEMORY = 128 # MB
MAX_MEMORY = 3008 # MB
MIN_REQUESTS = 0
MAX_REQUESTS = 1000
MIN_THROUGHPUT = 0 # % requests per sampling interval
MAX_THROUGHPUT = 100 # % requests per sampling interval
MIN_LATENCY = 0 # ms
MAX_LATENCY = 900000 # 15 minutes - 900000 ms
MIN_REWARD = -1000 # penalty for invalid actions
MAX_REWARD = 1000 # maximum reward for valid actions
MIN_UTILIZATION = 0 # % CPU/memory utilization
MAX_UTILIZATION = 100 # % CPU/memory utilization

MIN_ACTION = 0 # minimum number of replicas to scale
MAX_ACTION = 10 # maximum number of replicas to scale


SAMPLING_INTERVAL = 30 # seconds
FUNCTION_CPU_REQUEST = 100 # m
FUNCTION_MEMORY_REQUEST = 128 # MB
SUCCESS_CODE = 200 # HTTP status code for successful requests
EPISODES = 100 # number of episodes to run

# Default values for the Configuration problem
STATUS = ['Success', 'Failure']