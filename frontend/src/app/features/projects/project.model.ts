export interface Project {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}
export interface CreateProjectRequest {
  name: string;
  description: string | null;
}
export interface UpdateProjectRequest {
  name: string;
  description: string | null;
}

