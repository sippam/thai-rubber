import { Routes } from '@angular/router';
import { FollowDiseaseComponent } from './features/follow-disease/follow-disease.component';
import { LandingPageComponent } from './features/landing-page/landing-page.component';
import { DatabaseComponent } from './features/database/database.component';
import { AdaptiveModelComponent } from './features/adaptive-model/adaptive-model.component';
import { HomeComponent } from './features/home/home.component';
import { AuthGuard } from './core/guards/auth.guard';
import { CallbackComponent } from './features/callback/callback.component';

export const routes: Routes = [
  {
    path: '',
    component: LandingPageComponent,
  },
  {
    path: 'callback',
    component: CallbackComponent,
  },
  {
    path: 'home',
    component: HomeComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'follow-disease',
    component: FollowDiseaseComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'database',
    component: DatabaseComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'adaptive-model',
    component: AdaptiveModelComponent,
    canActivate: [AuthGuard],
  },
];
