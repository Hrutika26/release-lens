CREATE TABLE IF NOT EXISTS api_request (
    id BIGSERIAL PRIMARY KEY,

    release_environment_id BIGINT NOT NULL,

    request_id VARCHAR(255) NOT NULL,

    timestamp TIMESTAMPTZ NOT NULL,

    endpoint VARCHAR(500) NOT NULL,
    method VARCHAR(20) NOT NULL,

    status_code INTEGER NOT NULL,
    response_time_ms INTEGER NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_api_request_release_environment
        FOREIGN KEY (release_environment_id)
        REFERENCES release_environment(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_api_request
        UNIQUE (
            release_environment_id,
            request_id
        )
);