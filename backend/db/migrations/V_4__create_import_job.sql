CREATE TABLE IF NOT EXISTS import_job (
    id BIGSERIAL PRIMARY KEY,

    project_id BIGINT NOT NULL,

    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,

    version VARCHAR(100) NOT NULL,
    environment VARCHAR(50) NOT NULL,

    commit_sha VARCHAR(100),
    deployed_at TIMESTAMPTZ,

    status VARCHAR(50) NOT NULL,

    total_records BIGINT NOT NULL DEFAULT 0,
    processed_records BIGINT NOT NULL DEFAULT 0,
    valid_records BIGINT NOT NULL DEFAULT 0,
    invalid_records BIGINT NOT NULL DEFAULT 0,

    error_message TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,

    CONSTRAINT fk_import_job_project
        FOREIGN KEY (project_id)
        REFERENCES project(id)
        ON DELETE CASCADE
);