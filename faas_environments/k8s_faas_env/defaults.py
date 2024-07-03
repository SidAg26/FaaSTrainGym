import os

# Default values for the Kubernetes environment
CONFIG_FILE_PATH = '~/.kube/config'
KUBECONFIG = os.getenv('KUBECONFIG')
PROMETHEUS_URL = 'http://prometheus-server.monitoring.svc.cluster.local'
DEFAULT_NAMESPACE = 'openfaas-fn'
DEFAULT_DEPLOYMENT = 'gateway-external'

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
MIN_REWARD = -100 # penalty for invalid actions
MAX_REWARD = 10000 # maximum reward for valid actions

SAMPLING_INTERVAL = 30 # seconds