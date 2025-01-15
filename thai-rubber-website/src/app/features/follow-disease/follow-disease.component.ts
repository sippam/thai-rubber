import { AsyncPipe } from '@angular/common';
import { Component, inject, OnInit, SimpleChanges } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule, MatLabel } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatTableModule } from '@angular/material/table';
import { RouterLink } from '@angular/router';
import { NotificationService } from '@services/notification/notification.service';
import { UserService } from '@services/user/user.service';
import { map, Observable, startWith } from 'rxjs';
import { ThaiDatePipe } from 'src/app/shared/pipes/thai-date.pipe';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { DialogComponent } from './dialog/dialog.component';

interface Officer {
  id: number;
  name: string;
}
@Component({
  selector: 'app-follow-disease',
  standalone: true,
  imports: [
    MatIconModule,
    MatButtonModule,
    MatTableModule,
    RouterLink,
    ThaiDatePipe,
    MatPaginatorModule,
    MatFormFieldModule,
    MatLabel,
    MatInputModule,
    MatAutocompleteModule,
    ReactiveFormsModule,
    AsyncPipe,
    MatDialogModule,
  ],
  templateUrl: './follow-disease.component.html',
  styleUrl: './follow-disease.component.scss',
})
export class FollowDiseaseComponent implements OnInit {
  #notificationsService = inject(NotificationService);
  #userService = inject(UserService);
  displayedColumns: string[] = [
    'id',
    'name',
    'disease',
    'risk',
    'officer',
    'status',
    'detail',
    'date',
    'edit',
  ];

  dataSource = [
    {
      id: 1,
      name: 'John Doe',
      disease: 'Covid-19',
      risk: 'High',
      status: 'Positive',
      detail: 'Detail',
      date: '2021-08-01',
    },
  ];

  selectedOfficer: Officer | null = null;

  selectProvince(event: Officer) {
    this.selectedOfficer = event; // อัปเดต selectedProvince
  }

  // selectedValue: any = null;
  // options: Officer[] = [];
  // formControl = new FormControl(); // FormControl สำหรับควบคุม input
  // filteredFrom!: Observable<any[]>; // รายการข้อมูลที่กรองได้

  // ngOnChanges(changes: SimpleChanges): void {
  //   // ถ้า options เปลี่ยน รีเซ็ต filter
  //   if (changes['options'] && !changes['options'].firstChange) {
  //     this._setupFilter(); // โหลดตัวกรองใหม่
  //     this.formControl.setValue(''); // ล้างค่า input
  //   }
  // }

  // private _setupFilter(): void {
  //   this.filteredFrom = this.formControl.valueChanges.pipe(
  //     startWith(''),
  //     map((value) =>
  //       typeof value === 'string'
  //         ? this._filter(value, this.options)
  //         : this.options.slice()
  //     )
  //   );
  // }

  // // ฟังก์ชันกรองข้อมูล
  // private _filter(value: string, options: Officer[]): Officer[] {
  //   if (!options || options.length === 0) {
  //     return []; // ถ้าไม่มี options ให้คืนค่ากลับเป็น array ว่าง
  //   }

  //   const filterValue = value.toLowerCase(); // แปลงค่าที่กรอกเป็นตัวพิมพ์เล็ก
  //   return options.filter(
  //     (option) => option.name.toLowerCase().includes(filterValue) // กรองเฉพาะค่าที่ตรงกับคำที่กรอก
  //   );
  // }

  // // ฟังก์ชันเลือกค่า
  // selectValue(value: Officer, row: any): void {
  //   if (row && row.formControl) {
  //     // ตรวจสอบว่า formControl ถูกสร้าง
  //     row.formControl.setValue(value.name); // อัปเดตเฉพาะแถวนี้
  //     const officer_id = value.id;

  //     this.#notificationsService
  //       .updateOfficer(officer_id.toString(), row.id.toString())
  //       .subscribe({
  //         next: (response: any) => {
  //           console.log(`Officer updated for row ${row.id}:`, response);
  //         },
  //         error: (error) => {
  //           console.error(`Error updating officer for row ${row.id}:`, error);
  //         },
  //       });
  //   } else {
  //     console.error('FormControl is undefined for the row:', row);
  //   }
  // }

  // resetFilter(): void {
  //   if (!this.selectedValue) {
  //     this.formControl.setValue(''); // ล้างค่าหากไม่ได้เลือก
  //   }
  //   this._setupFilter(); // รีเฟรชรายการ
  // }

  pageSize = 10;
  pageIndex = 0;
  length = 0;

  ngOnInit(): void {
    this.getNoti();
    // this.#userService.getAllUsers().subscribe({
    //   next: (response: any) => {
    //     this.options = response.data;

    //     // เพิ่ม formControl และ filteredFrom ให้แต่ละแถว
    //     this.dataSource = this.dataSource.map((row) => ({
    //       ...row,
    //       formControl: new FormControl(''), // ตรวจสอบว่า formControl ถูกสร้าง
    //       filteredFrom: new Observable<Officer[]>(), // Observable สำหรับข้อมูลที่กรอง
    //     }));

    //     // ตั้งค่า filter สำหรับแต่ละแถว
    //     this.dataSource.forEach((row) => {
    //       this.setupFilter(row);
    //     });
    //   },
    //   error: (error) => {
    //     console.log(error);
    //   },
    // });
  }

  // setupFilter(row: any): void {
  //   row.filteredFrom = row.formControl.valueChanges.pipe(
  //     startWith(''),
  //     map((value: string) => this._filter(value || '', this.options))
  //   );
  // }

  onPageChange(event: PageEvent) {
    this.pageSize = event.pageSize;
    this.pageIndex = event.pageIndex;
    console.log('event.pageIndex', event.pageIndex);

    this.length = event.length;
    this.getNoti();
  }

  getNoti() {
    this.#notificationsService
      .getAllNotificatrtions(
        (this.pageIndex + 1).toString(),
        this.pageSize.toString()
      )
      .subscribe({
        next: (response: any) => {
          console.log('wow', response);

          this.dataSource = response.data;
          this.length = response.totalRows;
        },
        error: (error) => {
          console.log(error);
        },
      });
  }

  readonly dialog = inject(MatDialog);

  openDialog(notification_id: number) {
    const dialogRef = this.dialog.open(DialogComponent, {
      data: { notification_id: notification_id },
    });

    dialogRef.afterClosed().subscribe((result) => {
      console.log(`Dialog result: ${result}`);
      this.getNoti();
    });
  }
}
