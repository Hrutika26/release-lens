from pydantic import BaseModel


class MetricValueResponse(BaseModel):
    base_value: float | None
    target_value: float | None
    absolute_delta: float | None
    percentage_delta: float | None


class ReleaseComparisonSummaryResponse(BaseModel):
    total_requests: MetricValueResponse
    average_latency: MetricValueResponse
    p95_latency: MetricValueResponse
    p99_latency: MetricValueResponse
    error_rate: MetricValueResponse


class EndpointComparisonResponse(BaseModel):
    endpoint: str
    method: str

    request_count: MetricValueResponse

    average_latency: MetricValueResponse
    p50_latency: MetricValueResponse
    p95_latency: MetricValueResponse
    p99_latency: MetricValueResponse

    error_rate: MetricValueResponse
    client_error_rate: MetricValueResponse
    server_error_rate: MetricValueResponse


class ReleaseEnvironmentComparisonResponse(BaseModel):
    base_release_id: int
    base_release_environment_id: int
    base_version: str

    target_release_id: int
    target_release_environment_id: int
    target_version: str

    environment: str

    summary: ReleaseComparisonSummaryResponse

    endpoints: list[EndpointComparisonResponse]