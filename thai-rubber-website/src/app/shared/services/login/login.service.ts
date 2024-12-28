import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment as env } from '@environments/environment';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  constructor(private http: HttpClient) {}

  lineLogin(code: string) {
    return this.http.post(`${env.api_url}/line/login`, { code }).pipe();
  }

  getUserProfile(): Observable<any> {
    return this.http
      .get(`${env.api_url}/user/me`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      })
      .pipe();
  }

  register(data: any) {
    return this.http.post(`${env.api_url}/register`, data).pipe();
  }

  login(data: any) {
    return this.http.post(`${env.api_url}/login`, data).pipe();
  }
}
