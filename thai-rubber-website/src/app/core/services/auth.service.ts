import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { environment as env } from '@environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(private router: Router) {}

  loginWithLine(): void {
    const line_url = env.line_url;
    window.location.href = line_url;
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }

  // Logout
  logout(): void {
    localStorage.removeItem('access_token');
    this.router.navigate(['/']);
  }
}
