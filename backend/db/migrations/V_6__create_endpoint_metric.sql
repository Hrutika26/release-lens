CREATE TABLE IF NOT EXISTS endpoint_metric (
    id BIGSERIAL PRIMARY KEY,

    release_environment_id BIGINT NOT NULL,

    endpoint VARCHAR(500) NOT NULL,
    method VARCHAR(20) NOT NULL,

    request_count BIGINT NOT NULL,

    average_latency DOUBLE PRECISION,
    p50_latency DOUBLE PRECISION,
    p95_latency DOUBLE PRECISION,
    p99_latency DOUBLE PRECISION,

    error_rate DOUBLE PRECISION,
    client_error_rate DOUBLE PRECISION,
    server_error_rate DOUBLE PRECISION,

    additional_metrics JSONB NOT NULL DEFAULT '{}'::jsonb,

    metrics_version INTEGER NOT NULL DEFAULT 1,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_endpoint_metric_release_environment
        FOREIGN KEY (release_environment_id)
        REFERENCES release_environment(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_endpoint_metric
        UNIQUE (
            release_environment_id,
            method,
            endpoint
        )
);