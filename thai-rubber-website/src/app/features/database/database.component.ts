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
import {
  MatAutocompleteModule,
} from '@angular/material/autocomplete';
import { SearchSelectComponent } from '@components/search-select/search-select.component';
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

  #provincesService = inject(ProvinceService);
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
    { form_name: 'plating_area', label: 'พื้นที่ปลูก' },
    { form_name: 'name_rubber_type', label: 'ชื่อพันธุ์ยาง' },
    { form_name: 'area', label: 'ลักษณะพื้นที่' },
    { form_name: 'soil', label: 'ลักษณะดิน' },
    { form_name: 'disease_name', label: 'ชื่อโรค' },
    { form_name: 'disease_level', label: 'ระดับความรุนแรงของโรค' },
    { form_name: 'temperature', label: 'อุณหภูมิ' },
    { form_name: 'humidity', label: 'ความชื้นสัมพัทธ์' },
    { form_name: 'wind_speed', label: 'ความเร็วลม' },
    { form_name: 'wind_direction', label: 'ทิศทางลม' },
    { form_name: 'daily_rainfall', label: 'ปริมาณน้ำฝนต่อวัน' },
    { form_name: 'rainy_days_per_month', label: 'จำนวนวันที่ฝนตกต่อเดือน' },
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
      farmer_list: [false],
      plating_area: [false],
      name_rubber_type: [false],
      area: [false],
      soil: [false],
      disease_name: [false],
      disease_level: [false],
      temperature: [false],
      humidity: [false],
      wind_speed: [false],
      wind_direction: [false],
      daily_rainfall: [false],
      rainy_days_per_month: [false],
    });

    this.databaseGroup = this.fb.group({
      dicease: [''],
      disease_level: [''],
    });
  }

  ngOnInit() {
    // Fetch provinces and districts
    this.#provincesService.getAllProvinces().subscribe((data) => {
      this.provinces = data as Provinces[];
    });
  }

  selectProvince(event: Provinces) {
    const province_id = event.id;
    const district_data = this.provinces?.filter(
      (province) => province.id === province_id
    ) as Provinces[];
    const districts = district_data[0].amphure;
    this.districts = districts;

    this.filterGroup.patchValue({
      province: event.name_th,
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
      district: event.name_th,
      tambon: null,
    });

    this.selectedDistrict = event; // อัปเดตอำเภอ
    this.selectedTambon = null; // รีเซ็ตตำบล
  }

  selectTambon(event: Tambon) {
    this.filterGroup.patchValue({
      tambon: event.name_th,
    });

    this.selectedTambon = event; // อัปเดตตำบล
  }

  selectTypeRubber(event: { id: number; name_th: string }) {
    this.selectedTypeRubber = event;
    this.filterGroup.patchValue({
      rubber: event.name_th,
    });
  }
}
