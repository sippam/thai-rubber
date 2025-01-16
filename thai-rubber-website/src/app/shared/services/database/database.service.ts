import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment as env } from '@environments/environment';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root',
})
export class DatabaseService {
  http = inject(HttpClient);

  getCountPicture(dicease = '', sevirity = '') {
    return this.http.get(
      `${env.api_url}/count-picture?disease=${dicease}&sevirity=${sevirity}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      }
    );
  }

  getAllDatabaseTable(filterGroup: any, page: string, limit: string) {
    return this.http.post(
      `${env.api_url}/get-all?page=${page}&limit=${limit}`,
      {
        ...filterGroup,
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      }
    );
  }

  downloadCSV(filterGroup: any): Observable<Blob> {
    return this.http.post(
      `${env.api_url}/download-csv`,
      {
        ...filterGroup,
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        responseType: 'blob', // ต้องระบุว่าเป็นไฟล์
      }
    );
  }
}
