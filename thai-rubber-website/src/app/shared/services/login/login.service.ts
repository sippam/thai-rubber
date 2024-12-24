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

  getUserProfile(token: string): Observable<any> {
    return this.http
      .get(`${env.api_url}/line/profile/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .pipe();
  }
}
