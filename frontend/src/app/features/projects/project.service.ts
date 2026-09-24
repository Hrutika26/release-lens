import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { CreateProjectRequest, Project, UpdateProjectRequest } from './project.model';
import { environment } from '../../../environments/environment';
import { ImportConfirmResponse, ImportJobStatus, ImportPreview } from './release.model.import';
import { ReleaseDetail, ReleaseSummary } from './release.model';
import { EndpointMetric } from './endpoint-metric.model';
import { ReleaseEnvironmentComparison } from './release-comparison.model';

@Injectable({
  providedIn: 'root',
})
export class ProjectService {
  private readonly http = inject(HttpClient);

  private readonly apiUrl = environment.apiUrl;

  getProjects(): Observable<Project[]> {
    return this.http.get<Project[]>(
      `${this.apiUrl}/projects`
    );
  }

  createProject(request: CreateProjectRequest): Observable<Project> {
    return this.http.post<Project>(
      `${this.apiUrl}/projects`,
      request
    );
  }

  getProjectById(projectId: number): Observable<Project> {
    return this.http.get<Project>(
      `${this.apiUrl}/projects/${projectId}`
  );
  }

  updateProject(projectId: number, request: UpdateProjectRequest): Observable<Project> {
    return this.http.patch<Project>(
      `${this.apiUrl}/projects/${projectId}`,
      request
    );
  }

  previewReleaseImport(projectId: number, file: File): Observable<ImportPreview> {
    const formData = new FormData();

    formData.append('file', file);

    return this.http.post<ImportPreview>(
      `${this.apiUrl}/projects/${projectId}/release-imports/preview`,
      formData,
    );
  }


  confirmReleaseImport(projectId: number, importId: number): Observable<ImportConfirmResponse> {
    return this.http.post<ImportConfirmResponse>(
      `${this.apiUrl}/projects/${projectId}/release-imports/${importId}/confirm`,
      {},
    );
  }


  getReleaseImportStatus(projectId: number, importId: number): Observable<ImportJobStatus> {
    return this.http.get<ImportJobStatus>(
      `${this.apiUrl}/projects/${projectId}/release-imports/${importId}`,
    );
  }

  getReleases(projectId: number): Observable<ReleaseSummary[]> {
    return this.http.get<ReleaseSummary[]>(
      `${this.apiUrl}/projects/${projectId}/releases`,
    );
  }

  getRelease(projectId: number, releaseId: number): Observable<ReleaseDetail> {
    return this.http.get<ReleaseDetail>(
      `${this.apiUrl}/projects/${projectId}/releases/${releaseId}`,
    );
  }

  getEnvironmentMetrics(projectId: number, releaseId: number, environmentId: number): Observable<EndpointMetric[]> {
    return this.http.get<EndpointMetric[]>(
      `${this.apiUrl}/projects/${projectId}/releases/${releaseId}/environments/${environmentId}/metrics`,
    );
  }

  compareReleases(projectId: number, baseEnvironmentId: number, targetEnvironmentId: number): Observable<ReleaseEnvironmentComparison> {
    return this.http.get<ReleaseEnvironmentComparison>(
      `${this.apiUrl}/projects/${projectId}/releases/compare`,
      {
        params: {
          base_environment_id: baseEnvironmentId,
          target_environment_id: targetEnvironmentId,
        },
      },
    );
  }
}