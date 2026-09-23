from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class EndpointMetric:
    id: int
    release_environment_id: int
    endpoint: str
    method: str
    request_count: int
    average_latency: float | None
    p50_latency: float | None
    p95_latency: float | None
    p99_latency: float | None
    error_rate: float | None
    client_error_rate: float | None
    server_error_rate: float | None
    additional_metrics: dict[str, Any]
    metrics_version: int
    created_at: datetime
    updated_at: datetime