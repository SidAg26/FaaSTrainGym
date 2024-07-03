import os
import defaults
from kubernetes import client, config
from prometheus_api_client import PrometheusConnect

class Context:
    """
    A class representing the context for interacting with Kubernetes and Prometheus.

    Attributes:
        k8s_config (bool): A flag indicating whether the Kubernetes configuration has been loaded.
        k8s_scale_api (kubernetes.client.AppsV1Api): The Kubernetes scale API client.
        k8s_resource_api (kubernetes.client.CustomObjectsApi): The Kubernetes resource API client.
        prometheus_api (prometheus_api_client.PrometheusConnect): The Prometheus client.
        k8s_deployment_name (str): The Kubernetes deployment name.
        k8s_deployment_namespace (str): The Kubernetes deployment namespace.

    Methods:
        load_k8s_config: Loads the Kubernetes configuration.
        set_k8s_deployment_name: Sets the Kubernetes deployment name.
        set_k8s_deployment_namespace: Sets the Kubernetes deployment namespace.
        set_k8s_scale_api: Returns the Kubernetes scale API client.
        set_k8s_resource_api: Returns the Kubernetes resource API client.
        set_prometheus_api: Returns the Prometheus client.
        get_k8s_scale_api: Returns the Kubernetes scale API client.
        get_k8s_resource_api: Returns the Kubernetes resource API client.
        get_prometheus_api: Returns the Prometheus client.
        get_k8s_deployment_name: Returns the Kubernetes deployment name.
        get_k8s_deployment_namespace: Returns the Kubernetes deployment namespace.

    """

    def __init__(self):
        self.k8s_config = None # for loading k8s config
        
        self.k8s_scale_api = None # for scaling deployments
        self.k8s_resource_api = None # for getting resource usage
        self.prometheus_api = None # for getting/querying metrics from prometheus
        self.k8s_deployment_name = None # for storing the function deployment name
        self.k8s_deployment_namespace = None # for storing the function deployment namespace

# Setters

    def load_k8s_config(self) -> None:
        """
        Loads the Kubernetes configuration.

        If the configuration is not initialized, it loads the Kubernetes configuration.

        Returns:
            None
        """

        if self.k8s_config is False:
            try:
                if os.path.exists(os.path.expanduser(defaults.CONFIG_FILE_PATH)):
                    config.load_config()
                elif defaults.KUBECONFIG is not None:
                    config.load_kube_config(config_file=defaults.KUBECONFIG)
                else:
                    # Load in-cluster configuration only from inside a pod
                    config.load_incluster_config()
                self.k8s_config = True
            except Exception as e:
                print(f"Error loading Kubernetes configuration - check config file: {e}")

    def set_k8s_deployment_name(self, deployment_name: str) -> None:
        """
        Sets the Kubernetes deployment name.

        Args:
            deployment_name (str): The deployment name.

        Returns:
            None
        """
        self.k8s_deployment_name = deployment_name

    def set_k8s_deployment_namespace(self, deployment_namespace: str) -> None:
        """
        Sets the Kubernetes deployment namespace.

        Args:
            deployment_namespace (str): The deployment namespace.

        Returns:
            None
        """
        self.k8s_deployment_namespace = deployment_namespace

    def set_k8s_scale_api(self):
        """
        Returns the Kubernetes API client.

        If the client is not initialized, it loads the Kubernetes configuration and initializes the client.

        Returns:
            None
        """
        if self.k8s_config is False:
            self.load_k8s_config()
        if self.k8s_scale_api is None:
            try:
                self.k8s_scale_api = client.AppsV1Api() # for scaling deployments
            except Exception as e:
                print(f"Error loading Kubernetes scale client - check configuration: {e}")
    
    def set_k8s_resource_api(self):
        """
        Returns the Kubernetes API client.

        If the client is not initialized, it loads the Kubernetes configuration and initializes the client.

        Returns:
            None
        """
        if self.k8s_config is False:
            self.load_k8s_config()
        if self.k8s_resource_api is None:
            try:
                self.k8s_resource_api = client.CustomObjectsApi() # for getting resource usage
            except Exception as e:
                print(f"Error loading Kubernetes resource client - check configuration: {e}")
        
    def set_prometheus_api(self, url: str):
        """
        Returns the Prometheus client.

        If the client is not initialized, it initializes the client with the specified URL.

        Returns:
            prometheus_api_client.PrometheusConnect: The Prometheus client.
        """
        if self.prometheus_api is None:
            try:
                self.prometheus_api = PrometheusConnect(url=url, disable_ssl=True)
            except Exception as e:
                print(f"Error loading Prometheus client - falling back to default path {e}")
                try:
                    self.prometheus_api = PrometheusConnect(url=defaults.PROMETHEUS_URL, disable_ssl=True)
                except Exception as e:
                    print(f"Error loading Prometheus client - check default URL: {e}")

    
# Getters
    def get_k8s_scale_api(self):
        """
        Returns the Kubernetes scale API client.

        Returns:
            kubernetes.client.AppsV1Api: The Kubernetes scale API client.
        """
        if self.k8s_scale_api is None:
            self.set_k8s_scale_api()
        return self.k8s_scale_api
    
    def get_k8s_resource_api(self):
        """
        Returns the Kubernetes resource API client.

        Returns:
            kubernetes.client.CustomObjectsApi: The Kubernetes resource API client.
        """
        if self.k8s_resource_api is None:
            self.set_k8s_resource_api()
        return self.k8s_resource_api
    
    def get_prometheus_api(self):
        """
        Returns the Prometheus API client.

        Args:
            None

        Returns:
            prometheus_api_client.PrometheusConnect: The Prometheus client.
        """
        if self.prometheus_api is None:
            print("Prometheus API not set - falling back to default URL")
            return self.set_prometheus_api(defaults.PROMETHEUS_URL)
        return self.prometheus_api

    def get_k8s_deployment_name(self):
        """
        Returns the Kubernetes deployment name.

        Returns:
            str: The Kubernetes deployment name.
        """
        return self.k8s_deployment_name
    
    def get_k8s_deployment_namespace(self):
        """
        Returns the Kubernetes deployment namespace.

        Returns:
            str: The Kubernetes deployment namespace.
        """
        return self.k8s_deployment_namespace
    
    def main():
        # Create an instance of the Context class
        context = Context()

        # Set the Kubernetes deployment name and namespace
        context.set_k8s_deployment_name("my-deployment")
        context.set_k8s_deployment_namespace("my-namespace")

        # Load the Kubernetes configuration
        context.load_k8s_config()

        # Get the Kubernetes scale API client
        scale_api = context.get_k8s_scale_api()

        # Get the Kubernetes resource API client
        resource_api = context.get_k8s_resource_api()

        # Get the Prometheus API client
        prometheus_api = context.get_prometheus_api("http://prometheus.example.com")

        # Get the Kubernetes deployment name and namespace
        deployment_name = context.get_k8s_deployment_name()
        deployment_namespace = context.get_k8s_deployment_namespace()

        # Print the deployment name and namespace
        print(f"Deployment Name: {deployment_name}")
        print(f"Deployment Namespace: {deployment_namespace}")

    if __name__ == "__main__":
        main()
