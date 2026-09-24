import { Component, inject, TemplateRef } from '@angular/core';
import { ProjectService } from '../project.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Project, UpdateProjectRequest } from '../project.model';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { FormBuilder, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { ImportPreview } from '../release.model.import';
import { ReleaseSummary } from '../release.model';

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

  importPreview: ImportPreview | null = null;

  isPreviewingImport = false;
  isConfirmingImport = false;

  releases: ReleaseSummary[] = [];

  isLoadingReleases = false;

  importReleaseForm = this.formBuilder.group({
    file: [
      null as File | null,
      Validators.required,
    ],
  });

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
    this.loadReleases()
  }

  loadReleases(): void {
    const projectId = Number(
      this.route.snapshot.paramMap.get('id')
    );

    if (!projectId) {
      return;
    }

    this.isLoadingReleases = true;

    this.projectService
      .getReleases(projectId)
      .subscribe({
        next: releases => {
          this.releases = releases;
          this.isLoadingReleases = false;
        },

        error: error => {
          console.error(
            'Failed to load releases',
            error,
          );

          this.isLoadingReleases = false;
        },
      });
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

  onImportFileSelected(event: Event): void {
    const input =
      event.target as HTMLInputElement;

    const file =
      input.files?.[0] ?? null;

    this.importReleaseForm.patchValue({
      file,
    });

    this.importReleaseForm
      .controls.file
      .markAsTouched();
  }

  openImportReleaseModal(modal: TemplateRef<unknown>): void {
    this.importReleaseForm.reset();

    this.importPreview = null;

    this.modalRef =
      this.modalService.open(
        modal,
        {
          centered: true,
          size: 'md',
          backdrop: 'static',
        },
      );
  }

  previewReleaseImport(): void {
    if (
      this.importReleaseForm.invalid ||
      !this.project
    ) {
      this.importReleaseForm.markAllAsTouched();
      return;
    }

    const file =
      this.importReleaseForm
        .controls.file
        .value;

    if (!file) {
      return;
    }

    this.isPreviewingImport = true;

    this.projectService
      .previewReleaseImport(
        this.project.id,
        file,
      )
      .subscribe({
        next: preview => {
          this.importPreview = preview;
          this.isPreviewingImport = false;
        },

        error: error => {
          console.error(
            'Failed to preview release import',
            error,
          );

          this.isPreviewingImport = false;
        },
      });
  }

  confirmReleaseImport(): void {
    if (
      !this.project ||
      !this.importPreview
    ) {
      return;
    }

    this.isConfirmingImport = true;

    this.projectService
      .confirmReleaseImport(
        this.project.id,
        this.importPreview.import_id,
      )
      .subscribe({
        next: () => {
          this.isConfirmingImport = false;

          this.modalRef?.close();

          this.importReleaseForm.reset();
          this.importPreview = null;
          this.loadReleases()
        },

        error: error => {
          console.error(
            'Failed to confirm release import',
            error,
          );

          this.isConfirmingImport = false;
        },
      });
  }

  openRelease(releaseId: number): void {
  if (!this.project) {
    return;
  }

  this.router.navigate([
    '/projects',
    this.project.id,
    'releases',
    releaseId,
  ]);
}

openReleaseComparison(): void {
  if (!this.project) {
    return;
  }

  this.router.navigate([
    '/projects',
    this.project.id,
    'compare',
  ]);
}


}
