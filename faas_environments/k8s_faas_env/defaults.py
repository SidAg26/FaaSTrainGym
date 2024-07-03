import os

CONFIG_FILE_PATH = '~/.kube/config'
KUBECONFIG = os.getenv('KUBECONFIG')
PROMETHEUS_URL = 'http://prometheus-server.monitoring.svc.cluster.local'