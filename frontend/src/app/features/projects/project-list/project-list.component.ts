import { Component, inject } from '@angular/core';
import { ProjectService } from '../project.service';
import { Project } from '../project.model';

@Component({
  selector: 'app-project-list',
  imports: [],
  standalone: true,
  templateUrl: './project-list.component.html',
  styleUrl: './project-list.component.css'
})
export class ProjectListComponent {

  private readonly projectService = inject(ProjectService);

  projects: Project[] = [];

  ngOnInit(): void {
    this.loadProjects();
  }

  private loadProjects(): void {
    this.projectService.getProjects().subscribe({
      next: projects => {
        this.projects = projects;
      },
      error: error => {
        console.error('Failed to load projects', error);
      },
    });
  }

}
