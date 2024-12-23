import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { LoginService } from '@services/login/login.service';
import { UserService } from '@services/user/user.service';

@Component({
  selector: 'app-callback',
  standalone: true,
  imports: [],
  templateUrl: './callback.component.html',
  styleUrl: './callback.component.scss',
})
export class CallbackComponent implements OnInit {
  #loginService = inject(LoginService);
  #userService = inject(UserService);
  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    const code = this.route.snapshot.queryParamMap.get('code');
    if (code) {
      this.#loginService.lineLogin(code).subscribe((response: any) => {
        if (response) {
          const access_token = response.token.access_token;
          localStorage.setItem('access_token', access_token);
          console.log('access_token', access_token);

          this.fetchUserProfile(access_token);
        }
      });
    }
  }

  fetchUserProfile(token: string): void {
    this.#loginService.getUserProfile(token).subscribe(
      (profile) => {
        this.#userService.setUserProfile(profile);
        this.router.navigate(['/home']);
      },
      (error) => {
        console.error('Failed to fetch profile:', error);
        this.router.navigate(['/']); // ถ้าดึงโปรไฟล์ไม่สำเร็จให้ไปหน้า login
      }
    );
  }
}
