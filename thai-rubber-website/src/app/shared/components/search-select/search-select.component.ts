import { AsyncPipe, JsonPipe } from '@angular/common';
import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnInit,
  Output,
  SimpleChanges,
} from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { map, Observable, startWith } from 'rxjs';

@Component({
  selector: 'app-search-select',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatAutocompleteModule,
    AsyncPipe,
    MatFormField,
    MatInputModule,
    MatLabel,
  ],
  templateUrl: './search-select.component.html',
  styleUrl: './search-select.component.scss',
})
export class SearchSelectComponent implements OnInit, OnChanges {
  @Input() label: string = ''; // Label ของ input
  @Input() placeholder: string = ''; // Placeholder
  @Input() options: any[] = []; // ตัวเลือกที่ใช้กรอง
  @Input() selectedValue: any = null;
  @Output() valueSelected = new EventEmitter<any>(); // ส่งค่าที่เลือกกลับไป

  formControl = new FormControl(); // FormControl สำหรับควบคุม input
  filteredFrom!: Observable<any[]>; // รายการข้อมูลที่กรองได้

  ngOnInit(): void {
    this._setupFilter();
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
      option.name_th.toLowerCase().includes(filterValue)
    );
  }

  // ฟังก์ชันเลือกค่า
  selectValue(value: any): void {
    this.selectedValue = value; // เก็บค่าที่เลือก
    this.valueSelected.emit(value); // ส่งค่ากลับไปที่ component แม่
    this.formControl.setValue(value.name_th); // ตั้งค่าให้ input
  }

  resetFilter(): void {
    if (!this.selectedValue) {
      this.formControl.setValue(''); // ล้างค่าหากไม่ได้เลือก
    }
    this._setupFilter(); // รีเฟรชรายการ
  }  
}
