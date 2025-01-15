import { AsyncPipe } from '@angular/common';
import { Component, inject, signal, SimpleChanges } from '@angular/core';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { NotificationService } from '@services/notification/notification.service';
import { UserService } from '@services/user/user.service';
import { map, Observable, startWith } from 'rxjs';

@Component({
  selector: 'app-dialog',
  standalone: true,
  imports: [
    MatDialogModule,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule,
    MatAutocompleteModule,
    ReactiveFormsModule,
    AsyncPipe,
    FormsModule,
    MatSelectModule,
  ],
  templateUrl: './dialog.component.html',
  styleUrl: './dialog.component.scss',
})
export class DialogComponent {
  readonly data = inject(MAT_DIALOG_DATA);

  #userService = inject(UserService);
  #notificationsService = inject(NotificationService);
  formControl = new FormControl();
  filteredFrom!: Observable<any[]>; // รายการข้อมูลที่กรองได้
  selectedValue: any = null;
  options: any[] = [];
  datail: string = '';
  select_status: string = '';

  status_array = [
    { value: 'request_not_accept', text: 'ยังไม่ได้รับคำร้อง'},
    { value: 'process_of_contact', text: 'กำลังติดต่อ'},
    { value: 'process', text: 'กำลังดำเนินการ'},
    { value: 'explore', text: 'สำรวจ'},
    { value: 'follow_watchout', text: 'ติดตาม/ระวัง'},
    { value: 'heal', text: 'รักษา'},
  ]

  ngOnInit(): void {
    this._setupFilter();
    this.#userService.getAllUsers().subscribe({
      next: (response: any) => {
        this.options = response.data;
      },
      error: (error) => {
        console.log('error', error);
      },
    });

    this.#notificationsService
      .getSpecificNotification(this.data.notification_id)
      .subscribe({
        next: (response: any) => {
          const data = {
            id: response.data.officer_id,
            name: response.data.name,
          };
          this.selectedValue = data;
          this.formControl.setValue(response.data.name);
          this.select_status = response.data.status;
          this.datail = response.data.details;
        },
        error: (error) => {
          console.log('error', error);
        },
      });
  }

  ngOnChanges(changes: SimpleChanges): void {
    // ถ้า options เปลี่ยน รีเซ็ต filter
    if (changes['options'] && !changes['options'].firstChange) {
      this._setupFilter(); // โหลดตัวกรองใหม่
      this.formControl.setValue(''); // ล้างค่า input
    }
  }

  private _setupFilter(): void {
    this.filteredFrom = this.formControl.valueChanges.pipe(
      startWith(''),
      map((value) =>
        typeof value === 'string' ? this._filter(value) : this.options.slice()
      )
    );
  }

  // ฟังก์ชันกรองข้อมูล
  private _filter(value: string): any[] {
    const filterValue = value.toLowerCase();
    return this.options.filter((option) =>
      option.name.toLowerCase().includes(filterValue)
    );
  }

  // ฟังก์ชันเลือกค่า
  selectValue(value: any): void {
    this.selectedValue = value; // เก็บค่าที่เลือก
    this.formControl.setValue(value.name); // ตั้งค่าให้ input
  }

  resetFilter(): void {
    if (!this.selectedValue) {
      this.formControl.setValue(''); // ล้างค่าหากไม่ได้เลือก
    }
    this._setupFilter(); // รีเฟรชรายการ
  }

  update() {
    console.log('datail', this.datail);

    console.log('notification_id', this.data.notification_id);
    this.#notificationsService
      .updateNotification(
        this.data.notification_id,
        this.selectedValue.id,
        this.select_status,
        this.datail
      )
      .subscribe({
        next: (response: any) => {
          console.log('response', response);
        },
        error: (error) => {
          console.log('error', error);
        },
      });
  }
}
