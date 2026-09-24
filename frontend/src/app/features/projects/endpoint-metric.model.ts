export interface EndpointMetric {
  endpoint: string;
  method: string;
  request_count: number;

  average_latency: number | null;
  p50_latency: number | null;
  p95_latency: number | null;
  p99_latency: number | null;

  error_rate: number | null;
  client_error_rate: number | null;
  server_error_rate: number | null;

  additional_metrics: Record<string, unknown>;
  metrics_version: number;
}