import { Routes } from '@angular/router';
import { AppLayoutComponent } from './layout/app-layout/app-layout.component';
import { ProjectListComponent } from './features/projects/project-list/project-list.component';
import { ProjectDetailComponent } from './features/projects/project-detail/project-detail.component';

export const routes: Routes = [
    {
        path: '',
        component: AppLayoutComponent, 
        children: [
            {
                path: 'projects', 
                component: ProjectListComponent
            },
            {
                path: 'projects/:id',
                component: ProjectDetailComponent
            },
            {
                path: '',
                redirectTo: 'projects',
                pathMatch: 'full'
            }
        ] 
    }
];
