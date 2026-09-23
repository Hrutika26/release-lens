CREATE TABLE IF NOT EXISTS release_environment (
    id BIGSERIAL PRIMARY KEY,

    release_id BIGINT NOT NULL,

    environment VARCHAR(50) NOT NULL,
    deployed_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_release_environment_release
        FOREIGN KEY (release_id)
        REFERENCES release(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_release_environment
        UNIQUE (
            release_id,
            environment
        )
);