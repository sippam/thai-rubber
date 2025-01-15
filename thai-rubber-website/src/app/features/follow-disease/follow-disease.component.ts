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

  pageSize = 10;
  pageIndex = 0;
  length = 0;

  ngOnInit(): void {
    this.getNoti();
  }
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
