import {Component, OnInit, inject} from '@angular/core';

import {DecimalPipe, PercentPipe} from '@angular/common';
import {ComparisonBarChartComponent, ComparisonChartItem} from '../../../shared/comparison-bar-chart/comparison-bar-chart.component';

import {
  FormBuilder,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';

import {
  ActivatedRoute,
  Router,
} from '@angular/router';

import {
  ReleaseEnvironment,
  ReleaseSummary,
} from '../release.model';

import {
  ReleaseEnvironmentComparison,
} from '../release-comparison.model';

import {
  ProjectService,
} from '../project.service';


interface EnvironmentOption {
  releaseId: number;
  releaseVersion: string;

  environmentId: number;
  environment: string;
}


@Component({
  selector: 'app-release-comparison',
  standalone: true,

  imports: [
    ReactiveFormsModule,
    DecimalPipe,
    PercentPipe,
    ComparisonBarChartComponent
  ],

  templateUrl:
    './release-comparison.component.html',

  styleUrl:
    './release-comparison.component.css',
})
export class ReleaseComparisonComponent
  implements OnInit {

  private readonly route =
    inject(ActivatedRoute);

  private readonly router =
    inject(Router);

  private readonly projectService =
    inject(ProjectService);

  private readonly formBuilder =
    inject(FormBuilder);


  releases: ReleaseSummary[] = [];
  p95ChartData: ComparisonChartItem[] = [];

  errorRateChartData: ComparisonChartItem[] = [];
  environmentOptions:
    EnvironmentOption[] = [];

  baselineOptions:
    EnvironmentOption[] = [];


  comparison:
    ReleaseEnvironmentComparison | null = null;


  isLoadingReleases = false;

  isComparing = false;


  comparisonForm =
    this.formBuilder.group({

      targetEnvironmentId: [
        null as number | null,
        Validators.required,
      ],

      baseEnvironmentId: [
        null as number | null,
        Validators.required,
      ],

    });


  ngOnInit(): void {
    this.loadReleases();

    this.comparisonForm
      .controls.targetEnvironmentId
      .valueChanges
      .subscribe(
        targetEnvironmentId => {
          this.handleTargetChange(
            targetEnvironmentId,
          );
        },
      );
  }


  loadReleases(): void {
    const projectId =
      this.getProjectId();

    if (!projectId) {
      return;
    }

    this.isLoadingReleases = true;

    this.projectService
      .getReleases(projectId)
      .subscribe({
        next: releases => {
          this.releases = releases;

          this.environmentOptions =
            this.buildEnvironmentOptions(
              releases,
            );

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


  private buildEnvironmentOptions(
    releases: ReleaseSummary[],
  ): EnvironmentOption[] {

    return releases.flatMap(
      release =>
        release.environments.map(
          environment => ({
            releaseId: release.id,

            releaseVersion:
              release.version,

            environmentId:
              environment.id,

            environment:
              environment.environment,
          }),
        ),
    );
  }


  private handleTargetChange(
    targetEnvironmentId:
      number | null,
  ): void {

    this.comparison = null;

    this.comparisonForm
      .controls.baseEnvironmentId
      .reset(
        null,
        {
          emitEvent: false,
        },
      );


    if (!targetEnvironmentId) {
      this.baselineOptions = [];
      return;
    }


    const target =
      this.environmentOptions.find(
        option =>
          option.environmentId ===
          targetEnvironmentId,
      );


    if (!target) {
      this.baselineOptions = [];
      return;
    }


    this.baselineOptions =
      this.environmentOptions.filter(
        option =>
          option.environment ===
            target.environment &&

          option.releaseId !==
            target.releaseId,
      );
  }


  compare(): void {

    if (
      this.comparisonForm.invalid
    ) {
      this.comparisonForm
        .markAllAsTouched();

      return;
    }


    const projectId =
      this.getProjectId();

    const {
      baseEnvironmentId,
      targetEnvironmentId,
    } =
      this.comparisonForm
        .getRawValue();


    if (
      !projectId ||
      !baseEnvironmentId ||
      !targetEnvironmentId
    ) {
      return;
    }


    this.isComparing = true;
    this.comparison = null;


    this.projectService
      .compareReleases(
        projectId,
        baseEnvironmentId,
        targetEnvironmentId,
      )
      .subscribe({
        next: comparison => {

          this.comparison =
            comparison;

          this.buildChartData();

          this.isComparing = false;
        },

        error: error => {

          console.error(
            'Failed to compare releases',
            error,
          );

          this.isComparing = false;
        },
      });
  }


  goBack(): void {

    const projectId =
      this.getProjectId();

    if (!projectId) {
      return;
    }

    this.router.navigate([
      '/projects',
      projectId,
    ]);
  }


  private getProjectId():
    number {

    return Number(
      this.route.snapshot
        .paramMap
        .get('projectId'),
    );
  }
  private buildChartData(): void {
  if (!this.comparison) {
    this.p95ChartData = [];
    this.errorRateChartData = [];

    return;
  }

  this.p95ChartData =
    this.comparison.endpoints
      .filter(
        endpoint =>
          endpoint.p95_latency.base_value !== null ||
          endpoint.p95_latency.target_value !== null,
      )
      .map(endpoint => ({
        label:
          `${endpoint.method} ${endpoint.endpoint}`,

        base:
          endpoint.p95_latency.base_value ?? 0,

        target:
          endpoint.p95_latency.target_value ?? 0,
      }));


  this.errorRateChartData =
    this.comparison.endpoints
      .filter(
        endpoint =>
          endpoint.error_rate.base_value !== null ||
          endpoint.error_rate.target_value !== null,
      )
      .map(endpoint => ({
        label:
          `${endpoint.method} ${endpoint.endpoint}`,

        base:
          (
            endpoint.error_rate.base_value
            ?? 0
          ) * 100,

        target:
          (
            endpoint.error_rate.target_value
            ?? 0
          ) * 100,
      }));
}

}