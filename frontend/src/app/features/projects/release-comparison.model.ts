export interface MetricValue {
  base_value: number | null;
  target_value: number | null;
  absolute_delta: number | null;
  percentage_delta: number | null;
}

export interface ReleaseComparisonSummary {
  total_requests: MetricValue;
  average_latency: MetricValue;
  p95_latency: MetricValue;
  p99_latency: MetricValue;
  error_rate: MetricValue;
}

export interface EndpointComparison {
  endpoint: string;
  method: string;

  request_count: MetricValue;

  average_latency: MetricValue;
  p50_latency: MetricValue;
  p95_latency: MetricValue;
  p99_latency: MetricValue;

  error_rate: MetricValue;
  client_error_rate: MetricValue;
  server_error_rate: MetricValue;
}

export interface ReleaseEnvironmentComparison {
  base_release_id: number;
  base_release_environment_id: number;
  base_version: string;

  target_release_id: number;
  target_release_environment_id: number;
  target_version: string;

  environment: string;

  summary: ReleaseComparisonSummary;

  endpoints: EndpointComparison[];
}