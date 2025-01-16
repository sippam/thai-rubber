import { Component, ElementRef, inject, ViewChild } from '@angular/core';
import { MatIcon } from '@angular/material/icon';
import { RouterLink } from '@angular/router';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import { MatDatepickerModule } from '@angular/material/datepicker';
import {
  DateAdapter,
  MAT_DATE_FORMATS,
  MAT_DATE_LOCALE,
} from '@angular/material/core';
import { ThaiDateAdapter } from '../../shared/pipes/thai-date-adapter';
import { THAI_DATE_FORMATS } from '../../shared/pipes/thai-date-formats';
import { CommonModule, DatePipe, registerLocaleData } from '@angular/common';
import localeTh from '@angular/common/locales/th';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatButtonModule } from '@angular/material/button';
import { ProvinceService } from '../../shared/services/province/province.service';
import {
  District,
  Provinces,
  Tambon,
} from '../../shared/models/provinces.model';
import { SelectDropDownModule } from 'ngx-select-dropdown';
import { NgSelectModule } from '@ng-select/ng-select';
import { NgxMatSelectSearchModule } from 'ngx-mat-select-search';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { SearchSelectComponent } from '@components/search-select/search-select.component';
import { DatabaseService } from '@services/database/database.service';
import { ThaiDatePipe } from 'src/app/shared/pipes/thai-date.pipe';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
registerLocaleData(localeTh);

@Component({
  selector: 'app-database',
  standalone: true,
  imports: [
    MatIcon,
    RouterLink,
    FormsModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    ReactiveFormsModule,
    MatDatepickerModule,
    MatCheckboxModule,
    MatButtonModule,
    SelectDropDownModule,
    NgSelectModule,
    NgxMatSelectSearchModule,
    CommonModule,
    MatAutocompleteModule,
    SearchSelectComponent,
    ThaiDatePipe,
    MatTableModule,
    MatPaginatorModule,
  ],
  templateUrl: './database.component.html',
  styleUrl: './database.component.scss',
  providers: [
    { provide: DateAdapter, useClass: ThaiDateAdapter },
    { provide: MAT_DATE_LOCALE, useValue: 'th-TH' },
    { provide: MAT_DATE_FORMATS, useValue: THAI_DATE_FORMATS },
    DatePipe,
  ],
})
export class DatabaseComponent {
  filterGroup: FormGroup;
  factorGroup: FormGroup;
  databaseGroup: FormGroup;

  displayedColumns: string[] = [
    'transaction_id',
    'name',
    'disease',
    'area',
    'land_type',
    'soil_type',
    'rubber_type',
    'temperature_min',
    'temperature_max',
    'temperature_avg',
    'precipitation_sum',
    'wind_speed',
    'wind_direction',
    'wind_gust',
    'shortwave_radiation_sum',
    'relative_humidity',
    'soil_moisture',
    'sevirity',
    'forecast_7days',
    'forecast_14days',
    'risk',
    'create_at',
  ];

  #provincesService = inject(ProvinceService);
  #databaseService = inject(DatabaseService);
  provinces: Provinces[] = [];
  districts: District[] = [];
  tambons: Tambon[] = [];

  selectedProvince: Provinces | null = null;
  selectedDistrict: District | null = null;
  selectedTambon: Tambon | null = null;

  typeRubber = [
    { id: 1, name_th: 'RRIM 600' },
    { id: 2, name_th: 'RRIM 1200' },
    { id: 3, name_th: 'RRII 118' },
    { id: 4, name_th: 'RRIT 251' },
    { id: 5, name_th: 'PBM 24' },
    { id: 6, name_th: 'JVP 80' },
    { id: 7, name_th: 'RRIM 2025' },
    { id: 8, name_th: 'PB 350' },
    { id: 9, name_th: 'PB255' },
    { id: 10, name_th: 'PB260' },
    { id: 11, name_th: 'RRIC110' },
    { id: 12, name_th: 'PR255' },
    { id: 13, name_th: 'BPM24' },
    { id: 14, name_th: 'สงขลา36' },
    { id: 15, name_th: 'PB 235' },
    { id: 16, name_th: 'RRIT 226' },
    { id: 17, name_th: 'RRIT 400' },
    { id: 18, name_th: 'RRIT 401' },
    { id: 19, name_th: 'RRIT 402' },
    { id: 20, name_th: 'RRIT 403' },
    { id: 21, name_th: 'RRIT 209' },
    { id: 22, name_th: 'RRIT 214' },
    { id: 23, name_th: 'RRIT 218' },
    { id: 24, name_th: 'RRIT 225' },
    { id: 25, name_th: 'RRIT 250' },
    { id: 26, name_th: 'RRIT 319' },
    { id: 27, name_th: 'RRIT 405' },
    { id: 28, name_th: 'RRIT 406' },
    { id: 29, name_th: 'RRIC 100' },
    { id: 30, name_th: 'RRIC 101' },
    { id: 31, name_th: 'PR 302' },
    { id: 32, name_th: 'PR 305' },
    { id: 33, name_th: 'Haiken 2' },
    { id: 34, name_th: 'RRIT 312' },
    { id: 35, name_th: 'RRIT 325' },
    { id: 36, name_th: 'RRIT 404' },
    { id: 37, name_th: 'RRIT 407' },
    { id: 38, name_th: 'RRIT 409' },
    { id: 39, name_th: 'RRIC 121' },
    { id: 40, name_th: 'RRII118' },
    { id: 41, name_th: 'RRII 203' },
  ];

  selectedTypeRubber: { id: number; name_th: string } | null = null;

  @ViewChild('districtInput') districtInput!: ElementRef<HTMLInputElement>;

  factor_label = [
    { form_name: 'farmer_list', label: 'รายชื่อเกษตรกร' },
    { form_name: 'disease_name', label: 'ชื่อโรค' },
    { form_name: 'area', label: 'พื้นที่ปลูก' },
    { form_name: 'land_type', label: 'ลักษณะพื้นที่' },
    { form_name: 'soil_type', label: 'ลักษณะดิน' },
    { form_name: 'rubber_type', label: 'ชื่อพันธุ์ยาง' },
    { form_name: 'temperature', label: 'อุณหภูมิ' },
    { form_name: 'precipitation_sum', label: 'ปริมาณน้ำฝนสะสม' },
    { form_name: 'wind_speed', label: 'ความเร็วลม' },
    { form_name: 'wind_direction', label: 'ทิศทางลม' },
    { form_name: 'wind_gust', label: 'ความเร็วลมกระโชก' },
    { form_name: 'shortwave_radiation_sum', label: 'ปริมาณรังสีคลื่นสั้นสะสม' },
    { form_name: 'relative_humidity', label: 'ความชื้นสัมพัทธ์' },

    { form_name: 'sevirity', label: 'ระดับความรุนแรงของโรค' },
  ];

  constructor(private fb: FormBuilder) {
    this.filterGroup = this.fb.group({
      dicease: [''],
      province: [''],
      district: [''],
      tambon: [''],
      rubber: [''],
      start: [''],
      end: [''],
    });

    this.factorGroup = this.fb.group({
      disease_name: [true],
      farmer_list: [true],
      area: [true],
      land_type: [true],
      soil_type: [true],
      rubber_type: [true],
      temperature: [true],
      precipitation_sum: [true],
      wind_speed: [true],
      wind_direction: [true],
      wind_gust: [true],
      shortwave_radiation_sum: [true],
      relative_humidity: [true],
      sevirity: [true],
    });

    this.databaseGroup = this.fb.group({
      dicease: [''],
      disease_level: [''],
    });
  }

  countPicture = 0;
  dataSource = [
    {
      transaction_id: 1,
      disease: 'Covid-19',
      temperature_min: 30,
      temperature_max: 35,
      temperature_avg: 32,
      precipitation_sum: 10,
      wind_speed: 10,
      wind_direction: 11,
      wind_gust: 20,
      shortwave_radiation_sum: 30,
      relative_humidity: 40,
      soil_moisture: 50,
      sevirity: 1,
      forecast_7days: 1,
      forecast_14days: 1,
      risk: 1,
      create_at: '2021-08-01',
    },
  ];

  forecast_7_14_days_decode: { [key: number]: string } = {
    0: 'ไม่แสดงอาการ',
    1: 'ความรุนแรงระดับ 1',
    2: 'ความรุนแรงระดับ 2',
    3: 'ความรุนแรงระดับ 3',
    4: 'ร่องรอยซากโรค',
  };

  disease_decode(text: string) {
    const raw_text = text.split('ระยะ')[0].trim();
    const deocde_text = raw_text.includes('ราแป้ง') ? 'powder' : 'newfall';
    return deocde_text;
  }

  risk_docode: { [key: string]: { [key: number]: string } } = {
    powder: {
      0: 'ต่ำ',
      1: 'สูง',
    },
    newfall: {
      0: 'ต่ำ',
      1: 'ปานกลาง',
      2: 'สูง',
    },
  };

  pageSize = 10;
  pageIndex = 0;
  length = 0;

  ngOnInit() {
    // Fetch provinces and districts
    this.#provincesService.getAllProvinces().subscribe((data) => {
      this.provinces = data as Provinces[];
    });

    this.#databaseService.getCountPicture().subscribe({
      next: (response: any) => {
        this.countPicture = response.data;
      },
    });

    this.databaseGroup.valueChanges.subscribe((value) => {
      this.#databaseService
        .getCountPicture(value.dicease, value.disease_level)
        .subscribe({
          next: (response: any) => {
            this.countPicture = response.data;
          },
        });
    });

    this.filterGroup.valueChanges.subscribe((value) => {
      this.#databaseService
        .getAllDatabaseTable(
          value,
          (this.pageIndex + 1).toString(),
          this.pageSize.toString()
        )
        .subscribe({
          next: (response: any) => {
            this.dataSource = response.data;
            this.length = response.totalRows;
          },
        });
    });

    this.#databaseService
      .getAllDatabaseTable(
        this.filterGroup.value,
        (this.pageIndex + 1).toString(),
        this.pageSize.toString()
      )
      .subscribe({
        next: (response: any) => {
          this.dataSource = response.data;
          this.length = response.totalRows;
        },
      });
  }

  onPageChange(event: PageEvent) {
    this.pageSize = event.pageSize;
    this.pageIndex = event.pageIndex;
    console.log('event.pageIndex', event.pageIndex);

    this.length = event.length;
  }

  selectProvince(event: Provinces) {
    const province_id = event.id;
    const district_data = this.provinces?.filter(
      (province) => province.id === province_id
    ) as Provinces[];
    const districts = district_data[0].amphure;
    this.districts = districts;

    this.filterGroup.patchValue({
      province: event.name_en,
      district: null,
      tambon: null,
    });

    this.selectedProvince = event; // อัปเดต selectedProvince
    this.selectedDistrict = null; // รีเซ็ตอำเภอ
    this.selectedTambon = null; // รีเซ็ตตำบล
  }

  selectDistrict(event: District) {
    const district_id = event.id;
    const tambon_data = this.districts?.filter(
      (district) => district.id === district_id
    ) as District[];
    const tambons = tambon_data[0].tambon;
    this.tambons = tambons;

    this.filterGroup.patchValue({
      district: event.name_en,
      tambon: null,
    });

    this.selectedDistrict = event; // อัปเดตอำเภอ
    this.selectedTambon = null; // รีเซ็ตตำบล
  }

  selectTambon(event: Tambon) {
    this.filterGroup.patchValue({
      tambon: event.name_en,
    });

    this.selectedTambon = event; // อัปเดตตำบล
  }

  selectTypeRubber(event: { id: number; name_th: string }) {
    this.selectedTypeRubber = event;
    this.filterGroup.patchValue({
      rubber: event.name_th,
    });
  }

  download() {
    window.open('http://localhost:3000/api/download-zip', '_blank');
  }

  handleDownloadCSV() {
    this.#databaseService.downloadCSV(this.filterGroup.value).subscribe({
      next: (response: Blob) => {
        const blob = new Blob([response], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);

        // สร้างลิงก์สำหรับดาวน์โหลดไฟล์
        const a = document.createElement('a');
        a.href = url;
        a.download = 'data.csv';
        a.click();

        // ลบ URL หลังจากใช้งาน
        window.URL.revokeObjectURL(url);
      },
      error: (err) => {
        console.error('Error downloading CSV:', err);
      },
    });
  }
}
