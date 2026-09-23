import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { CreateProjectRequest, Project, UpdateProjectRequest } from './project.model';
import { environment } from '../../../environments/environment';
import { ImportConfirmResponse, ImportJobStatus, ImportPreview } from './release.model.import';
import { ReleaseSummary } from './release.model';

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


}