import { Routes } from '@angular/router';
import { AppLayoutComponent } from './layout/app-layout/app-layout.component';
import { ProjectListComponent } from './features/projects/project-list/project-list.component';

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
                path: '',
                redirectTo: 'projects',
                pathMatch: 'full'
            }
        ]
    }
];
