from abc import ABC, abstractmethod



class MetricsCollection(ABC):
    def __init__(self, sampling_window: int, success_code: int):
        assert sampling_window > 0, 'Sampling window must be greater than zero.'
        self.sampling_window = sampling_window
        self.success_code = success_code

    @abstractmethod
    def set_success_code(self, success_code: int):
        pass

    @abstractmethod
    def set_function_name(self, function_name: str):
        pass

    @abstractmethod
    def set_sampling_window(self, sampling_window: int):
        pass

    @abstractmethod
    def get_latency(self) -> float:
        pass

    @abstractmethod
    def get_throughput(self, total_requests:int | None) -> int:
        pass

    @abstractmethod
    def get_requests(self) -> int:
        pass

    @abstractmethod
    def get_replicas(self) -> int:
        pass

    @abstractmethod
    def get_cpu_utilization(self) -> float:
        pass

    @abstractmethod
    def get_memory_utilization(self) -> float:
        pass