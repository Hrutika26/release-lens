export interface ReleaseEnvironment {
  id: number;
  release_id: number;
  environment: string;
  deployed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface ReleaseSummary {
  id: number;
  project_id: number;
  version: string;
  commit_sha: string | null;
  created_at: string;
  updated_at: string;

  environments: ReleaseEnvironment[];
}