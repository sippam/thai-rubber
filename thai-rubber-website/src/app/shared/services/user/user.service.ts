import { Injectable } from '@angular/core';
import { UserProfile } from '../../models/user.model';
import { HttpClient } from '@angular/common/http';
import { environment as env } from '@environments/environment.development';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private userProfileSubject = new BehaviorSubject<any>(null); // เก็บข้อมูลโปรไฟล์
  userProfile$: Observable<any> = this.userProfileSubject.asObservable(); // ให้ component อื่น subscribe ได้

  // เซ็ตโปรไฟล์ใหม่
  setUserProfile(profile: any): void {
    this.userProfileSubject.next(profile);
  }

  // ดึงโปรไฟล์ปัจจุบัน
  getUserProfile(): any {
    return this.userProfileSubject.value;
  }

  // ล้างข้อมูลโปรไฟล์เมื่อ logout
  clearUserProfile(): void {
    this.userProfileSubject.next(null);
  }
}
