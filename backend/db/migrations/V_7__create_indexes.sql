CREATE UNIQUE INDEX IF NOT EXISTS idx_project_name
    ON project (name);

CREATE INDEX IF NOT EXISTS idx_release_environment_deployed_at
    ON release_environment (deployed_at);

CREATE INDEX IF NOT EXISTS idx_import_job_project
    ON import_job (project_id);

CREATE INDEX IF NOT EXISTS idx_import_job_project_created_at
    ON import_job (project_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_import_job_status
    ON import_job (status);


CREATE INDEX IF NOT EXISTS idx_api_request_environment_timestamp
    ON api_request (
        release_environment_id,
        timestamp
    );

CREATE INDEX IF NOT EXISTS idx_api_request_environment_endpoint
    ON api_request (
        release_environment_id,
        method,
        endpoint
    );

CREATE INDEX IF NOT EXISTS idx_api_request_environment_status
    ON api_request (
        release_environment_id,
        status_code
    );