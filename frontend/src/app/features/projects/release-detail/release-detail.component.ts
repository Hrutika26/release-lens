import { DatePipe, DecimalPipe, PercentPipe } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { EndpointMetric } from '../endpoint-metric.model';

import {
  ReleaseDetail,
  ReleaseEnvironment,
} from '../release.model';
import { ProjectService } from '../project.service';


@Component({
  selector: 'app-release-detail',
  standalone: true,
  imports: [
    DatePipe,
    DecimalPipe,
    PercentPipe
  ],
  templateUrl: './release-detail.component.html',
  styleUrl: './release-detail.component.css',
})
export class ReleaseDetailComponent implements OnInit {

  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly projectService = inject(ProjectService);

  release: ReleaseDetail | null = null;

  selectedEnvironment: ReleaseEnvironment | null = null;

  isLoading = false;

  metrics: EndpointMetric[] = [];

  isLoadingMetrics = false;


  ngOnInit(): void {
    this.loadRelease();
  }


  loadRelease(): void {
    const projectId = Number(
      this.route.snapshot.paramMap.get('projectId'),
    );

    const releaseId = Number(
      this.route.snapshot.paramMap.get('releaseId'),
    );

    if (!projectId || !releaseId) {
      return;
    }

    this.isLoading = true;

    this.projectService
      .getRelease(
        projectId,
        releaseId,
      )
      .subscribe({
        next: release => {
          this.release = release;

          this.selectedEnvironment =
            release.environments[0] ?? null;

          this.isLoading = false;
          if (this.selectedEnvironment) {
            this.loadMetrics(this.selectedEnvironment);
          }
        },

        error: error => {
          console.error(
            'Failed to load release',
            error,
          );

          this.isLoading = false;
        },
      });
  }

  loadMetrics(environment: ReleaseEnvironment): void {
    const projectId = Number(
      this.route.snapshot.paramMap.get('projectId'),
    );

    const releaseId = Number(
      this.route.snapshot.paramMap.get('releaseId'),
    );

    if (!projectId || !releaseId) {
      return;
    }

    this.isLoadingMetrics = true;

    this.projectService
      .getEnvironmentMetrics(
        projectId,
        releaseId,
        environment.id,
      )
      .subscribe({
        next: metrics => {
          this.metrics = metrics;
          this.isLoadingMetrics = false;
        },

        error: error => {
          console.error(
            'Failed to load metrics',
            error,
          );

          this.metrics = [];
          this.isLoadingMetrics = false;
        },
      });
  }


  selectEnvironment(
    environment: ReleaseEnvironment,
  ): void {
    this.selectedEnvironment = environment;
    this.loadMetrics(this.selectedEnvironment)
  }




  goBack(): void {
    const projectId = Number(
      this.route.snapshot.paramMap.get('projectId'),
    );

    if (!projectId) {
      return;
    }

    this.router.navigate([
      '/projects',
      projectId,
    ]);
  }

  get totalRequests(): number {
  return this.metrics.reduce(
    (total, metric) =>
      total + metric.request_count,
    0,
  );
}


get endpointCount(): number {
  return this.metrics.length;
}


get averageLatency(): number | null {
  const totalRequests = this.totalRequests;

  if (!totalRequests) {
    return null;
  }

  const weightedLatency =
    this.metrics.reduce(
      (total, metric) => {
        if (metric.average_latency === null) {
          return total;
        }

        return total +
          (
            metric.average_latency *
            metric.request_count
          );
      },
      0,
    );

  return weightedLatency / totalRequests;
}


get errorRate(): number | null {
  const totalRequests = this.totalRequests;

  if (!totalRequests) {
    return null;
  }

  const weightedErrors =
    this.metrics.reduce(
      (total, metric) => {
        if (metric.error_rate === null) {
          return total;
        }

        return total +
          (
            metric.error_rate *
            metric.request_count
          );
      },
      0,
    );

  return weightedErrors / totalRequests;
}
}
