import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment as env } from '@environments/environment';
@Injectable({
  providedIn: 'root',
})
export class NotificationService {
  http = inject(HttpClient);

  getAllNotificatrtions(page: string, limit: string) {
    return this.http.get(
      `${env.api_url}/follow-disease?page=${page}&limit=${limit}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      }
    );
  }

  updateNotification(
    notification_id: string,
    officer_id: string,
    detail: string
  ) {
    return this.http.post(
      `${env.api_url}/update-notification`,
      {
        officer_id,
        notification_id,
        detail,
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      }
    );
  }

  getSpecificNotification(id: string) {
    return this.http.get(`${env.api_url}/notification?id=${id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    });
  }
}
