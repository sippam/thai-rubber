import { JsonPipe } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { UserService } from '@services/user/user.service';
import { UserProfile } from '../../models/user.model';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    JsonPipe,
    MatButtonModule,
    MatCardModule,
    MatChipsModule,
    MatProgressBarModule,
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss',
})
export class NavbarComponent implements OnInit {
  userProfile: UserProfile | null = null;
  isMenuOpen = false;

  constructor(private userService: UserService, private router: Router) {}

  ngOnInit(): void {
    this.userService.userProfile$.subscribe((profile) => {
      if (profile && profile.status === 200) {
        this.userProfile = profile.profile; // รับข้อมูลโปรไฟล์แบบ reactive
      }
    });
  }

  toggleMenu() {
    this.isMenuOpen = !this.isMenuOpen;
  }

  // Logout และล้างข้อมูล
  logout(): void {
    localStorage.removeItem('access_token'); // ลบ token
    this.userService.clearUserProfile(); // ล้างโปรไฟล์จาก service
    window.location.href = '/';
  }
}
