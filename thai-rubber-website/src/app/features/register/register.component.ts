import {
  ChangeDetectionStrategy,
  Component,
  inject,
  signal,
} from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { Router } from '@angular/router';
import {
  swalError,
  swalLoading,
  swalLoadingClose,
  swalSuccess,
} from '@components/sweetalert/sweetalert';
import { LoginService } from '@services/login/login.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    ReactiveFormsModule,
    FormsModule,
  ],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RegisterComponent {
  #loginService = inject(LoginService);
  router = inject(Router);

  hidepassword = signal(true);

  clickTogglePassword(event: MouseEvent) {
    this.hidepassword.set(!this.hidepassword());
    event.stopPropagation();
  }

  hidepassword_confirm = signal(true);

  clickTogglePasswordConfirm(event: MouseEvent) {
    this.hidepassword_confirm.set(!this.hidepassword_confirm());
    event.stopPropagation();
  }

  fb = inject(FormBuilder);
  register: FormGroup = this.fb.group(
    {
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      password_confirm: ['', [Validators.required, Validators.minLength(6)]],
      name: ['', [Validators.required]],
      tel: [
        '',
        [
          Validators.required,
          Validators.pattern('^[0-9]{10}$'), // Accept exactly 10 digits (0-9 only)
        ],
      ],
      position: ['', [Validators.required]],
    },
    {
      validators: this.matchValidator('password', 'password_confirm'),
    }
  );

  onInputTel(event: any): void {
    // Replace any non-numeric characters dynamically
    const input = event.target.value.replace(/[^0-9]/g, '');
    this.register.get('tel')?.setValue(input); // Update value in FormControl
  }
  
  // Getter สำหรับ password
  get password() {
    return this.register.get('password');
  }

  // Getter สำหรับ password_confirm
  get passwordConfirm() {
    return this.register.get('password_confirm');
  }

  get passwordsNotMatch() {
    const password = this.password?.value;
    const confirmPassword = this.passwordConfirm?.value;
    return password && confirmPassword && password !== confirmPassword;
  }

  matchValidator(
    controlName: string,
    matchingControlName: string
  ): ValidatorFn {
    return (abstractControl: AbstractControl) => {
      const control = abstractControl.get(controlName);
      const matchingControl = abstractControl.get(matchingControlName);

      if (
        matchingControl!.errors &&
        !matchingControl!.errors?.['confirmedValidator']
      ) {
        return null;
      }

      if (control!.value !== matchingControl!.value) {
        const error = { confirmedValidator: 'รหัสผ่านไม่ตรงกัน' };
        matchingControl!.setErrors(error);
        return error;
      } else {
        matchingControl!.setErrors(null);
        return null;
      }
    };
  }

  onSubmit() {
    console.log('FormGroup Errors:', this.register.errors); // Debug Error ของ FormGroup
    if (this.register.valid) {
      swalLoading();
      this.#loginService.register(this.register.value).subscribe({
        next: (response: any) => {
          if (response.status == 201) {
            swalLoadingClose();
            swalSuccess('สมัครสมาชิกสำเร็จ').then(() => {
              this.router.navigate(['/login']);
            });
          }
        },
        error: (error) => {
          if (error.status == 400) {
            swalLoadingClose();
            swalError('อีเมลนี้ถูกลงทะเบียนแล้ว');
            console.log('Email already registered');
          }
        },
      });
    } else {
      console.log('Form is invalid', this.register.errors); // Debug Error ทั้งหมด
    }
  }
}
