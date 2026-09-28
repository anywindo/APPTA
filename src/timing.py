import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.perf_counter_ns()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter_ns()

    @property
    def elapsed_ns(self):
        if self.start_time is None or self.end_time is None:
            raise ValueError("Timer has not completed")
        return self.end_time - self.start_time

def calculate_throughput(message_size_bytes, latency_ns):
    """Calculates throughput in bytes per second."""
    if latency_ns == 0:
        return 0.0
    latency_s = latency_ns / 1_000_000_000.0
    return message_size_bytes / latency_s
