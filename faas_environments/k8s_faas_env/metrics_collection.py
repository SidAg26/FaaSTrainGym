from .context import Context
import defaults as defaults

import math as math


class MetricsCollection:
    def __init__(self, ctx: Context, sampling_window: int = defaults.SAMPLING_INTERVAL):
        self.ctx = ctx
        assert sampling_window > 0, 'Sampling window must be greater than zero.'
        self.sampling_window = sampling_window
        self.success_code = defaults.SUCCESS_CODE

        self.k8s_resource_api = self.ctx.get_k8s_resource_api() 
        self.prometheus_api = self.ctx.get_prometheus_api()

        self._function_name = self.ctx.get_k8s_deployment_name()
        self._function_namespace = self.ctx.get_k8s_deployment_namespace()
        self.function_name = f"{self._function_name}.{self._function_namespace}"
         

    def set_success_code(self, success_code: int):
        assert success_code, 'Success code cannot be empty.'
        self.success_code = success_code

    def set_function_name(self, function_name: str):
        assert function_name, 'Function name cannot be empty.'
        self.function_name = function_name


    def set_sampling_window(self, sampling_window: int):
        assert sampling_window > 0, 'Sampling window must be greater than zero.'
        self.sampling_window = sampling_window

    def get_latency(self) -> float:
        query = f"""
                (rate(gateway_functions_seconds_sum{{function_name='{self.function_name}', code='{self.success_code}'}}[{self.sampling_window}s])
                /
                rate(gateway_functions_seconds_count{{function_name='{self.function_name}', code='{self.success_code}'}}[{self.sampling_window}s]))
                """
        try:
            data = round(float((self.prometheus_api.custom_query(query)[0]['value'][1])), 3)
            avg_execution = {True:0, False: avg_execution}[math.isnan(data)]
            return avg_execution
        except Exception as _:
            print("Error getting latency")
            return 0.0
        

    def get_throughput(self, total_requests:int | None) -> int:
        query = f"""
                increase(gateway_function_invocation_total{{code={self.success_code}, function_name='{self.function_name}'}}[{self.sampling_window}s])
                """
        if total_requests is None:
            total_requests = self.get_requests()
        try:
            data = int(float(self.prometheus_api.custom_query(query)[0]['value'][1]))
            throughput = int(round((data/total_requests)*100, 2))
            return throughput
        except ZeroDivisionError as _:
            print("Zero division error")
            return 100 if total_requests == 0 else 0
        except Exception as _:
            print("Error getting throughput")
            return 100 if total_requests == 0 else 0
            
        

    def get_requests(self) -> int:
        query = f"""
                increase(gateway_function_invocation_total{{function_name='{self.function_name}'}}[{self.sampling_window}s])
                """
        try:
            data = self.prometheus_api.custom_query(query)
            _total_requests = 0
            for d in data:
                _total_requests += int(float(d['value'][1]))
            return _total_requests
        except Exception as _:
            print("Error getting requests")
            return 0

    def get_replicas(self) -> int:
        # can also be done using the openfaas gateway_service_count metric
        query = f"""
                sum(kube_deployment_status_replicas{{deployment='{self._function_name}', namespace='{self._function_namespace}', phase='Running'}})
                """
        try:
            replicas = int(float(self.prometheus_api.custom_query(query)[0]['value'][1]))
            return replicas
        except Exception as _:
            print("Error getting replicas")
            return 0
        
    def _get_resource_list(self):
        try:
            resource_list = self.k8s_resource_api.list_namespaced_custom_object("metrics.k8s.io", 
                                                                                        "v1beta1", 
                                                                                        f"{self._function_namespace}", 
                                                                                        "pods")
            resource_list  = [pod['containers'][0]['usage'] for pod in resource_list['items'] if pod['metadata']['labels']['faas_function'] == self._function_namespace]
        except  Exception as _:
            print("Error getting resource list")
            resource_list = []
        return resource_list
    
    def get_cpu_utilization(self, func_cpu: int = defaults.FUNCTION_CPU_REQUEST):
        resource_list = self._get_resource_list()
        if not resource_list:
            print("No resources in the list")
            return 0
        cpu_utilization = 0.0
        for resource in resource_list:
            cpu = resource['cpu']
            try:
                # converting everything in to millicores (m) 1 vCPU = 1000m
                if cpu.endswith('n'):
                    cpu_utilization += (round(int(cpu.split('n')[0])/1e6, 4))
                elif cpu.endswith('u'):
                    cpu_utilization += (round(int(cpu.split('u')[0])/1e3, 4))
                elif cpu.endswith('m'):
                    cpu_utilization += (round(int(cpu.split('m')[0]), 4))
                else:
                    cpu_utilization += 0
            except Exception as _:
                print(f"Error getting cpu utilization from resource {resource['name']}")
                cpu_utilization += 0
        # default function cpu request is in millicores (m)
        return round((cpu_utilization/len(resource_list))/func_cpu, 4)

    def get_memory_utilization(self, func_mem: int = defaults.FUNCTION_MEMORY_REQUEST):
        resource_list = self._get_resource_list()
        if not resource_list:
            print("No resources in the list")
            return 0
        memory_utilization = 0.0
        for resource in resource_list:
            memory = resource['memory']
            try:
                # converting everything in to Gi
                if memory.endswith('Ki'):
                    memory_utilization += (round(int(memory.split('Ki')[0])/1024*1024, 4))
                elif memory.endswith('Mi'):
                    memory_utilization += (round(int(memory.split('Mi')[0])/1024, 4))
                elif memory.endswith('Gi'):
                    memory_utilization += (round(int(memory.split('Gi')[0]), 4))
                else:
                    memory_utilization += 0
            except Exception as _:
                print(f"Error getting memory utilization from resource {resource['name']}")
                memory_utilization += 0
        # default function memory request is in MB
        # converting everything in to Gi
        func_mem = round(func_mem / 1024, 2)
        return round((memory_utilization/len(resource_list))/func_mem, 4)