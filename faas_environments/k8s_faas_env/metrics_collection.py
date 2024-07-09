from .context import Context
from .defaults import defaults


class MetricsCollection:
    def __init__(self, ctx: Context):
        self.ctx = ctx

    def get_latency(self):
        return self.ctx.get_prometheus_api().get_latency()

    def get_throughput(self):
        return self.ctx.get_prometheus_api().get_throughput()

    def get_requests(self):
        return self.ctx.get_prometheus_api().get_requests()

    def get_replicas(self):
        return self.ctx.get_prometheus_api().get_replicas()

    def get_cpu_utilization(self):
        return self.ctx.get_prometheus_api().get_cpu_utilization()

    def get_memory_utilization(self):
        return self.ctx.get_prometheus_api().get_memory_utilization()