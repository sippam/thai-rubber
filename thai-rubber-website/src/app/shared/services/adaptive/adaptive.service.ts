import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment as env } from '@environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AdaptiveService {
  #http = inject(HttpClient);

  getAdaptivePlotPowder(disease: string, from?: string, to?: string) {
    return this.#http.get(
      `${env.api_url}/adaptive?disease=${disease}&from=${from}&to=${to}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      }
    );
  }

  getAdaptiveTable(disease: string) {
    return this.#http.get(
      `${env.api_url}/adaptive-table?disease=${disease}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      }
    );
  }
}
