import time
from functools import wraps
from typing import Callable

from prometheus_client import Counter, Histogram, start_http_server


NODE_CALLS = Counter("node_calls_total", "Total node calls", ["node"]) 
NODE_ERRORS = Counter("node_errors_total", "Total node errors", ["node"]) 
NODE_LATENCY = Histogram("node_latency_seconds", "Latency per node (s)", ["node"]) 


def instrument(node_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapped(*args, **kwargs):
            NODE_CALLS.labels(node=node_name).inc()
            start_time = time.perf_counter()
            try:
                return func(*args, **kwargs)
            except Exception:
                NODE_ERRORS.labels(node=node_name).inc()
                raise
            finally:
                duration = time.perf_counter() - start_time
                NODE_LATENCY.labels(node=node_name).observe(duration)
        return wrapped
    return decorator


def start_metrics_server(port: int = 9100) -> None:
    start_http_server(port)


__all__ = ["instrument", "start_metrics_server"]


