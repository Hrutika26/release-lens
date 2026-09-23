CREATE TABLE IF NOT EXISTS release (
    id BIGSERIAL PRIMARY KEY,

    project_id BIGINT NOT NULL,

    version VARCHAR(100) NOT NULL,
    commit_sha VARCHAR(100),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_release_project
        FOREIGN KEY (project_id)
        REFERENCES project(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_release_project_version
        UNIQUE (project_id, version)
);