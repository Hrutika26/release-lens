import { Component, inject, TemplateRef } from '@angular/core';
import { ProjectService } from '../project.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Project, UpdateProjectRequest } from '../project.model';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { FormBuilder, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-project-detail',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './project-detail.component.html',
  styleUrl: './project-detail.component.css'
})

export class ProjectDetailComponent {

  private readonly route = inject(ActivatedRoute);

  private readonly router = inject(Router);

  private readonly projectService = inject(ProjectService);

  project?: Project;

  isLoading = false;

  private readonly formBuilder = inject(FormBuilder);

  private readonly modalService = inject(NgbModal);

  modalRef?: NgbModalRef;

  isUpdating = false;

  editProjectForm = this.formBuilder.group({
    name: [
      '',
      [
        Validators.required,
        Validators.maxLength(255),
      ],
    ],

    description: [''],
  });

  ngOnInit(): void {
    this.loadProject();
  }

  loadProject() {

    const projectId = Number(
      this.route.snapshot.paramMap.get('id')
    );

    this.isLoading = true;

    this.projectService
      .getProjectById(projectId)
      .subscribe({
        next: project => {
          this.project = project;
          this.isLoading = false;
        },

        error: error => {
          console.error(
            'Failed to load project',
            error
          );

          this.isLoading = false;
        },
      });

  }

  goBack(): void {
    this.router.navigate(['/projects']);
  }

  updateProject() {
    if (
      this.editProjectForm.invalid ||
      !this.project
    ) {
      this.editProjectForm.markAllAsTouched();
      return;
    }

    const formValue =
      this.editProjectForm.getRawValue();

    const request: UpdateProjectRequest = {
      name: formValue.name!.trim(),

      description:
        formValue.description?.trim()
          ? formValue.description.trim()
          : null,
    };

    this.isUpdating = true;

    this.projectService
      .updateProject(
        this.project.id,
        request
      )
      .subscribe({
        next: updatedProject => {

          this.project = updatedProject;

          this.isUpdating = false;

          this.modalRef?.close();
        },

        error: error => {

          console.error(
            'Failed to update project',
            error
          );

          this.isUpdating = false;
        },
      });
  }

  openEditProjectModal(
    modal: TemplateRef<unknown>
  ): void {

    if (!this.project) {
      return;
    }

    this.editProjectForm.setValue({
      name: this.project.name,
      description:
        this.project.description ?? '',
    });

    this.modalRef =
      this.modalService.open(
        modal,
        {
          centered: true,
          size: 'md',
          backdrop: 'static',
        }
      );
  }


}
