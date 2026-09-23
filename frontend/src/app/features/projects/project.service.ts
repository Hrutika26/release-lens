import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { CreateProjectRequest, Project, UpdateProjectRequest } from './project.model';
import { environment } from '../../../environments/environment';

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
}