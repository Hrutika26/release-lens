export interface ImportValidation {
  total_records: number;
  valid_records: number;
  invalid_records: number;
}


export interface ImportReleaseMetadata {
  version: string;
  commit_sha: string | null;
}


export interface ImportEnvironmentMetadata {
  name: string;
  deployed_at: string | null;
}


export interface ImportPreview {
  import_id: number;
  file_name: string;
  status: string;

  release: ImportReleaseMetadata;
  environment: ImportEnvironmentMetadata;
  validation: ImportValidation;

  can_import: boolean;
}


export interface ImportConfirmResponse {
  import_id: number;
  status: string;
  message: string;
}


export interface ImportJobStatus {
  import_id: number;
  status: string;

  total_records: number;
  processed_records: number;
  valid_records: number;
  invalid_records: number;

  error_message: string | null;

  created_at: string;
  started_at: string | null;
  completed_at: string | null;
}