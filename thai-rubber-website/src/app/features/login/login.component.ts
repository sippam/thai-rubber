import { Component, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import {
  ReactiveFormsModule,
  FormsModule,
  FormBuilder,
  FormGroup,
  Validators,
  ValidatorFn,
  AbstractControl,
} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { Router } from '@angular/router';
import { LoginService } from '@services/login/login.service';
import { UserService } from '@services/user/user.service';
import { merge } from 'rxjs';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    ReactiveFormsModule,
    FormsModule,
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent {
  #loginService = inject(LoginService);
  #userService = inject(UserService);
  router = inject(Router);
  hide = signal(true);
  clickEvent(event: MouseEvent) {
    this.hide.set(!this.hide());
    event.stopPropagation();
  }

  fb = inject(FormBuilder);
  login: FormGroup = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
  });

  errorMessage = signal('');

  get email() {
    return this.login.get('email'); // ดึงข้อมูล email จาก FormGroup
  }

  // Getter สำหรับ password
  get password() {
    return this.login.get('password');
  }

  constructor() {
    // Subscribe เพื่อตรวจสอบการเปลี่ยนแปลงค่าและสถานะ
    merge(this.email!.statusChanges, this.email!.valueChanges)
      .pipe(takeUntilDestroyed())
      .subscribe(() => {
        this.updateErrorMessage();
      });
  }

  updateErrorMessage() {
    const emailErrors = this.email?.errors; // ดึงข้อผิดพลาดจาก email

    if (emailErrors?.['required']) {
      this.errorMessage.set('Email is required'); // ข้อความเมื่อไม่กรอก Email
    } else if (emailErrors?.['email']) {
      this.errorMessage.set('Invalid email format'); // ข้อความเมื่อรูปแบบ Email ไม่ถูกต้อง
    } else {
      this.errorMessage.set(''); // ลบข้อความเมื่อไม่มีข้อผิดพลาด
    }
  }

  onSubmit() {
    console.log('FormGroup Errors:', this.login.errors); // Debug Error ของ FormGroup
    if (this.login.valid) {
      this.#loginService.login(this.login.value).subscribe({
        next: (response: any) => {
          if (response.status == 200) {
            console.log('Login Success:', response);
            
            this.#userService.setUserProfile(response.data);
            localStorage.setItem('access_token', response.token);
            this.router.navigate(['/home']);
          }
        },
        error: (error: any) => {
          console.log('Error:', error);
        },
      });
    } else {
      console.log('Form is invalid', this.login.errors); // Debug Error ทั้งหมด
    }
  }
}
