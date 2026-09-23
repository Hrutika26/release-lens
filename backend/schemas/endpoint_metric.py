from typing import Any

from pydantic import BaseModel


class EndpointMetricResponse(BaseModel):
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