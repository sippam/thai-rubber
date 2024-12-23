import { Component, OnInit } from '@angular/core';
import { NavigationEnd, Router, RouterOutlet } from '@angular/router';
import { NavbarComponent } from './shared/components/navbar/navbar.component';
import { LoginService } from '@services/login/login.service';
import { UserService } from '@services/user/user.service';
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnInit {
  title = 'thai-rubber-website';
  hideNavbar = false; // ซ่อน Navbar เมื่อเป็น true

  constructor(
    private loginService: LoginService,
    private userService: UserService,
    private router: Router
  ) {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        // เช็ค path ปัจจุบัน
        const hiddenRoutes = ['/', '/callback'];
        console.log(
          'hiddenRoutes.includes(event.url)',
          hiddenRoutes.includes(event.url)
        );

        this.hideNavbar = hiddenRoutes.includes(event.url);
      }
    });
  }

  ngOnInit(): void {
    const accessToken = localStorage.getItem('access_token'); // ดึง token จาก localStorage

    if (accessToken && !this.userService.getUserProfile()) {
      // ดึงข้อมูลโปรไฟล์ถ้ายังไม่มีใน service
      this.loginService.getUserProfile(accessToken).subscribe(
        (profile) => {
          this.userService.setUserProfile(profile); // เซ็ตโปรไฟล์ใน service
        },
        (error) => {
          console.error('Failed to fetch profile:', error);
        }
      );
    }
  }
}
