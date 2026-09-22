import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Project } from './project.model';
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
}