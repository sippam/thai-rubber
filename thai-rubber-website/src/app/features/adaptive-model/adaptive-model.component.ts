import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatIcon } from '@angular/material/icon';
import { MatOption, MatSelect } from '@angular/material/select';
import { RouterLink } from '@angular/router';
import { SearchSelectComponent } from '@components/search-select/search-select.component';
import { ProvinceService } from '@services/province/province.service';
import {
  Provinces,
  District,
  Tambon,
} from 'src/app/shared/models/provinces.model';

@Component({
  selector: 'app-adaptive-model',
  standalone: true,
  imports: [
    MatIcon,
    RouterLink,
    MatFormField,
    MatLabel,
    MatSelect,
    MatOption,
    ReactiveFormsModule,
    SearchSelectComponent,
  ],
  templateUrl: './adaptive-model.component.html',
  styleUrl: './adaptive-model.component.scss',
})
export class AdaptiveModelComponent implements OnInit {
  filterGroup: FormGroup;

  filter_label = [
    { form_name: 'province', label: 'จังหวัด' },
    { form_name: 'district', label: 'อำเภอ' },
    { form_name: 'tambon', label: 'ตำบล' },
  ];
  #provincesService = inject(ProvinceService);
  provinces: Provinces[] = [];
  districts: District[] = [];
  tambons: Tambon[] = [];

  selectedProvince: Provinces | null = null;
  selectedDistrict: District | null = null;
  selectedTambon: Tambon | null = null;

  mockData = {
    farmer: 'นายกอไก่ ขอไข่',
    address: 'ม.6 ต.สังคม อ.สังคม จ.หนองคาย',
    area: '20 ไร่',
    area_characteristic: 'ลาดชัน',
    soil: 'ร่วนเหนียว',
    rubber_type: 'RRIM 600',
  };

  constructor(private fb: FormBuilder) {
    this.filterGroup = this.fb.group({
      province: [''],
      district: [''],
      tambon: [''],
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
}
