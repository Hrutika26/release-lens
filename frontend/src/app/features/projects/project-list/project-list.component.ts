import { Component, inject, TemplateRef } from '@angular/core';
import { ProjectService } from '../project.service';
import { CreateProjectRequest, Project } from '../project.model';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';

@Component({
  selector: 'app-project-list',
  imports: [ReactiveFormsModule],
  standalone: true,
  templateUrl: './project-list.component.html',
  styleUrl: './project-list.component.css'
})
export class ProjectListComponent {

  private readonly projectService = inject(ProjectService);

  private readonly formBuilder = inject(FormBuilder);

  private readonly modalService = inject(NgbModal);

  private readonly router = inject(Router);

  modalRef?: NgbModalRef;
  isLoading = false;
  isCreating = false;

  projectForm = this.formBuilder.group({
    name: [
      '',
      [
        Validators.required,
        Validators.maxLength(255),
      ],
    ],

    description: [''],
  });

  projects: Project[] = [];

  ngOnInit(): void {
    this.loadProjects();
  }

  private loadProjects(): void {
    this.isLoading = true
    this.projectService.getProjects().subscribe({
      next: projects => {
        this.projects = projects;
        this.isLoading = false
      },
      error: error => {
        console.error('Failed to load projects', error);
        this.isLoading = false
      },
    });
  }

  createProject() {
    if (this.projectForm.invalid) {
      this.projectForm.markAllAsTouched();
      return;
    }

    const formValue = this.projectForm.getRawValue();

    const request: CreateProjectRequest = {
      
      name: formValue.name!.trim(),

      description:
        formValue.description?.trim()
          ? formValue.description.trim()
          : null,
    };

    this.isCreating = true;

    this.projectService
      .createProject(request)
      .subscribe({
        next: project => {
          this.projects = [
            project,
            ...this.projects,
          ];

          this.isCreating = false;

          this.projectForm.reset();

          this.modalRef?.close();
        },

        error: error => {
          console.error(
            'Failed to create project',
            error
          );

          this.isCreating = false;
        },
      });
  }
  
  openCreateProjectModal(model: TemplateRef<unknown>) {
    this.projectForm.reset()

    this.modalRef =
      this.modalService.open(
        model,
        {
          centered: true,
          size: 'md',
          backdrop: 'static',
        }
      );
  }

  openProject(projectId: number){
    this.router.navigate([
    '/projects',
    projectId,
  ]);
  }

}


